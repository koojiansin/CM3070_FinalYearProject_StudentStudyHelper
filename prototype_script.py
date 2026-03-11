import os
import argparse
import whisper 
from moviepy.editor import VideoFileClip
from PIL import Image
# IMPORTS FOR BLIP
import torch 
from transformers import BlipProcessor, BlipForConditionalGeneration
# import json
import time # For exponential backoff
# import base64 # For base64 encoding/decoding
import requests # Import requests for synchronous HTTP calls
import shutil
from dotenv import load_dotenv

# --- OCR IMPORT & TESSERACT CONFIG ---
try:
    import pytesseract
except ImportError:
    print("PyTesseract not found. Please ensure it is installed (`pip install pytesseract`) and that Tesseract OCR is installed on your system.")
    pytesseract = None

# Default Windows install location (common)
_TESSERACT_DEFAULT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ensure_tesseract_configured():
    """Ensure pytesseract can find the Tesseract binary. Returns True if configured."""
    if pytesseract is None:
        return False

    found = shutil.which("tesseract")
    if found:
        try:
            pytesseract.pytesseract.tesseract_cmd = found
            return True
        except Exception:
            pass

    # Fallback to the common Windows install path
    if os.path.exists(_TESSERACT_DEFAULT):
        try:
            pytesseract.pytesseract.tesseract_cmd = _TESSERACT_DEFAULT
            return True
        except Exception:
            pass

    # Not configured
    try:
        pytesseract.pytesseract.tesseract_cmd = None
    except Exception:
        pass
    return False

# Run on import to provide a helpful warning if not available
_TESSERACT_OK = ensure_tesseract_configured()
if not _TESSERACT_OK:
    print("WARNING: Tesseract binary not found. OCR will be disabled until Tesseract is installed or configured.\n")

# --- CONFIGURATION ---
INPUT_VIDEO_PATH = "input_lecture.mp4"
TEMP_DIR = "temp_assets"
FRAME_INTERVAL_SECONDS = 5 

# --- LLM CONFIGURATION ---
LLM_MODEL = "gemini-2.5-flash"
# API_KEY = "AIzaSyCiUnxoApCcLvdFjnmv5KWgGQn11L_-Dsk" # Leave empty, will be provided at runtime
API_KEY = os.getenv("GEMINI_API_KEY")
STUDY_GUIDE_PATH = os.path.join(TEMP_DIR, "study_guide.md")
AUDIO_TEXT_PATH = os.path.join(TEMP_DIR, "audio_transcript.txt")
VISUAL_TEXT_PATH = os.path.join(TEMP_DIR, "visual_captions.txt")

# Set device to CPU if CUDA is available or we want stability
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# --- MODEL 1: WHISPER SETUP (Audio) ---
WHISPER_MODEL = "small" 
print(f"Loading Whisper model '{WHISPER_MODEL}' to {DEVICE}...")
try:
    # Load the Whisper model once
    whisper_model = whisper.load_model(WHISPER_MODEL, device=DEVICE)
except Exception as e:
    print(f"Could not load Whisper model: {e}")
    whisper_model = None


# --- MODEL 2: BLIP SETUP (Visual - Description) ---
# Initialize the BLIP processor and model
print("Loading BLIP model and processor...")
try:
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    # Using 'base' for a balance of speed and accuracy
    blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(DEVICE)
except Exception as e:
    print(f"Could not load BLIP model: {e}")
    processor = None
    blip_model = None

# --- Helper Functions ---
def setup_directories():
    """Ensure temporary asset directories exist."""
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(os.path.join(TEMP_DIR, "frames"), exist_ok=True)
    print(f"Setup complete. Temporary files saved to {TEMP_DIR}/")

def extract_audio(video_path):
    """Extracts the audio track from the video using moviepy."""
    print("Extracting audio from video...")
    audio_path = os.path.join(TEMP_DIR, "audio.mp3")
    try:
        video_clip = VideoFileClip(video_path)
        video_clip.audio.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        print(f"Error during audio extraction: {e}")
        return None

def extract_keyframes(video_path, interval):
    """Extracts a frame every 'interval' seconds."""
    print(f"Extracting keyframes every {interval} seconds...")
    frame_dir = os.path.join(TEMP_DIR, "frames")
    frames = []
    try:
        clip = VideoFileClip(video_path)
        duration = clip.duration
        
        for t in range(0, int(duration), interval):
            # Format the time for the filename (e.g., 0005s)
            time_str = f"{t:04d}s" 
            frame_path = os.path.join(frame_dir, f"frame_{time_str}.jpg")
            
            # Use save_frame for more control over format
            clip.save_frame(frame_path, t=t)
            frames.append({"path": frame_path, "timestamp": t})
            
        print(f"Extracted {len(frames)} frames.")
        return frames
    except Exception as e:
        print(f"Error during keyframe extraction: {e}")
        return []

def run_whisper_transcription(audio_path):
    """Runs Whisper on the audio file to get a time-stamped transcript."""
    if not whisper_model or not audio_path:
        return []
    print("Running Whisper ASR...")
    
    try:
        # Use a more detailed segment output format
        result = whisper_model.transcribe(audio_path, verbose=False)
        transcripts = []
        for segment in result.get("segments", []):
            # Only extract segment-level information for simplicity in the prototype
            transcripts.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip(),
                "words": segment.get("words", []) # Optional: include word-level data if available
            })
        print(f"Whisper transcription complete with {len(transcripts)} segments.")
        return transcripts
    except Exception as e:
        print(f"Error during Whisper transcription: {e}")
        return []

# --- NEW FUNCTION FOR OCR EXTRACTION ---
def run_ocr_extraction(frame_path):
    """Runs Tesseract OCR on a keyframe to extract text."""
    if not pytesseract:
        return "OCR tool not available."
    try:
        # Open the image using PIL
        img = Image.open(frame_path)
        
        # --- Image Pre-processing for better OCR results ---
        # 1. Convert to grayscale
        img = img.convert('L')
        # 2. Binarization (optional, but often helpful for contrast)
        # threshold = 127 # Simple threshold
        # img = img.point(lambda x: 0 if x < threshold else 255, '1')
        
        # Run Tesseract with custom config for potentially better results on lecture slides
        # The 'psm 6' configuration assumes a single uniform block of text.
        custom_config = r'--oem 3 --psm 6' 
        extracted_text = pytesseract.image_to_string(img, config=custom_config)
        
        # Clean up the output text
        cleaned_text = ' '.join(extracted_text.split()).strip()
        
        return cleaned_text
    except Exception as e:
        # If OCR fails (e.g., file permissions, bad format), return empty string
        return f"[OCR Error: {e}]"


def run_visual_analysis(frames):
    """Runs BLIP and OCR on extracted keyframes."""
    if not processor or not blip_model:
        return []
        
    print(f"Running BLIP (Captioning) and OCR (Text Extraction) on {len(frames)} frames...")
    captions = []
    
    for i, frame in enumerate(frames):
        try:
            image = Image.open(frame["path"]).convert('RGB')
            
            # 1. BLIP Captioning (General Description)
            inputs = processor(image, return_tensors="pt").to(DEVICE)
            out = blip_model.generate(**inputs, max_length=50)
            blip_caption = processor.decode(out[0], skip_special_tokens=True)
            
            # 2. OCR Extraction (Detailed Text)
            ocr_text = run_ocr_extraction(frame["path"])
            
            # Combine the results
            captions.append({
                "timestamp": frame["timestamp"],
                "path": frame["path"],
                "blip_description": blip_caption,
                "ocr_extracted_text": ocr_text 
            })
            print(f"  Frame {i+1}/{len(frames)} at {frame['timestamp']}s: Caption='{blip_caption[:30]}...' OCR='{ocr_text[:30]}...'")

        except Exception as e:
            print(f"Error processing frame {frame['timestamp']}s: {e}")
            captions.append({
                "timestamp": frame["timestamp"],
                "path": frame["path"],
                "blip_description": "[Analysis Failed]",
                "ocr_extracted_text": "[Analysis Failed]"
            })
            
    return captions

# --- Data Export Functions ---

def export_audio_data_to_text(transcript_data):
    """Exports structured transcript data to a text file for LLM ingestion."""
    print(f"Exporting audio data to {AUDIO_TEXT_PATH}...")
    try:
        with open(AUDIO_TEXT_PATH, 'w', encoding='utf-8') as f:
            for segment in transcript_data:
                # Format: [START_TIME]-[END_TIME] Audio: Spoken Text
                f.write(f"[{segment['start']:.2f}-{segment['end']:.2f}] Audio: {segment['text']}\n")
        print("Audio data export successful.")
    except Exception as e:
        print(f"Error exporting audio data: {e}")

def export_visual_data_to_text(visual_data):
    """Exports structured visual data to a text file for LLM ingestion."""
    print(f"Exporting visual data to {VISUAL_TEXT_PATH}...")
    try:
        with open(VISUAL_TEXT_PATH, 'w', encoding='utf-8') as f:
            for frame in visual_data:
                # Format: [KEYFRAME_TIME] Visual: [BLIP CAPTION] || OCR Text: [EXTRACTED TEXT]
                # The LLM will use the OCR Text for factual content and the BLIP caption for context.
                f.write(f"[{frame['timestamp']:.2f}] Visual: {frame['blip_description']} || OCR Text: {frame['ocr_extracted_text']}\n")
        print("Visual data export successful.")
    except Exception as e:
        print(f"Error exporting visual data: {e}")

# --- LLM Synthesis Function (Synchronous for Prototype) ---

def generate_study_guide(audio_path, visual_path, max_retries=5):
    """
    Synchronously calls the Gemini API to perform the multimodal synthesis.
    This simulates Stage 4 of the pipeline.
    """
    print(f"--- Stage 4: LLM Synthesis Engine ({LLM_MODEL}) ---")
    
    if not os.path.exists(audio_path) or not os.path.exists(visual_path):
        return "Synthesis skipped: Missing audio or visual input files."

    try:
        with open(audio_path, 'r', encoding='utf-8') as f:
            audio_text = f.read()
        with open(visual_path, 'r', encoding='utf-8') as f:
            visual_text = f.read()
            
    except Exception as e:
        return f"Error reading input files for LLM: {e}"

    # The prompt explicitly instructs the model to fuse the data and prioritize factual text from OCR
    system_prompt = (
        "You are an expert educational resource synthesizer. Your task is to take a time-synchronised, "
        "multimodal data stream (Audio Transcript and Visual/OCR Text) from a lecture and generate a "
        "structured, comprehensive, and chronologically ordered Study Guide in Markdown format. "
        "Crucially, fuse the 'Audio' and 'Visual' events by time. Prioritize and use the content from 'OCR Text' "
        "over the general 'Visual' description for all factual or textual information (like code, equations, or bullet points). "
        "Output ONLY the Markdown content for the study guide."
    )

    user_query = (
        f"Synthesize the following lecture data into a study guide. "
        f"Use headings, bullet points, and code blocks as appropriate.\n\n"
        f"--- AUDIO TRANSCRIPT ---\n{audio_text}\n\n"
        f"--- VISUAL/OCR DATA ---\n{visual_text}\n"
    )

    # API Request Setup
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{LLM_MODEL}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }

    # Exponential Backoff Retry Loop
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=60)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            
            result = response.json()
            
            # Extract content
            text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '').strip()
            
            if text:
                # Save the final study guide
                with open(STUDY_GUIDE_PATH, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Study Guide successfully generated and saved to {STUDY_GUIDE_PATH}")
                return text
            else:
                raise Exception("LLM returned an empty response.")

        except requests.exceptions.RequestException as e:
            # Handle connectivity or HTTP errors
            print(f"Attempt {attempt + 1} failed (Request Error): {e}")
        except Exception as e:
            # Handle JSON parsing or empty response errors
            print(f"Attempt {attempt + 1} failed (Processing Error): {e}")

        if attempt < max_retries - 1:
            delay = 2 ** attempt
            time.sleep(delay)
        else:
            print("Maximum retries reached. Synthesis failed.")
            return "Error: Could not generate study guide from LLM after multiple retries."


# --- Preview Generation Function (Stage 5 Simulation) ---

def generate_web_preview(transcript_data, visual_data):
    """
    Generates a single, fused, chronological timeline preview
    by merging ASR segments and visual events by time. (RQ1 validation)
    """
    
    # 1. Prepare all events
    all_events = []
    
    # Add Audio Events
    for segment in transcript_data:
        all_events.append({
            "time": segment["start"],
            "type": "AUDIO",
            "content": f"[Spoken: {segment['text']}]"
        })

    # Add Visual Events (now includes OCR text)
    for frame in visual_data:
        # Use a combination of BLIP and OCR for the preview to validate both steps
        content = (
            f"Visual: {frame['blip_description']} "
            f"| OCR Text: {frame['ocr_extracted_text']}"
        )
        all_events.append({
            "time": frame["timestamp"],
            "type": "VISUAL",
            "content": content
        })

    # 2. Sort all events chronologically
    all_events.sort(key=lambda x: x["time"])
    
    # 3. Format into a readable timeline
    preview_text = "--- Fused Multimodal Timeline (RQ1 Validation) ---\n"
    for event in all_events:
        preview_text += f"[T={event['time']:.2f}s] ({event['type']}) {event['content']}\n"
        
    return preview_text


# --- Main Execution Block (for local testing) ---

def main_execution(video_path):
    """Main execution flow for the prototype."""
    try:
        # 1. Setup & Extraction (Stage 1 & 2)
        setup_directories()
        if not os.path.exists(video_path):
            print(f"Error: Video file not found at {video_path}")
            return
            
        audio = extract_audio(video_path)
        frames = extract_keyframes(video_path, FRAME_INTERVAL_SECONDS)
        
        # 2. Analyze
        transcript = run_whisper_transcription(audio)
        captions = run_visual_analysis(frames) 
        
        # 3. Export Data
        export_audio_data_to_text(transcript) 
        export_visual_data_to_text(captions) 

        # 4. Generate Study Guide (synchronous execution simulation - Stage 4 & 5)
        study_guide_result = generate_study_guide(AUDIO_TEXT_PATH, VISUAL_TEXT_PATH)

        # 5. Preview
        # The preview now shows the combined analysis timeline and the study guide result
        preview_output = generate_web_preview(transcript, captions)
        preview_output += "\n--- GENERATED STUDY GUIDE (Saved to study_guide.md) ---\n"
        preview_output += study_guide_result
        
        print(preview_output)
        
    except Exception as e:
        print(f"An unexpected error occurred in main execution: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CM3070 Student Study Helper Prototype.")
    parser.add_argument("--video", type=str, default=INPUT_VIDEO_PATH, help="Path to the input video file.")
    args = parser.parse_args()
    
    main_execution(args.video)