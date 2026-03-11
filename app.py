# import os
# from flask import Flask, render_template, request, jsonify
# from werkzeug.utils import secure_filename
# import prototype_script
# import asyncio # Need asyncio to run the async function in a sync environment

# app = Flask(__name__)

# # Configuration
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/')
# def index():
#     return render_template('index.html')

# # We make the route asynchronous to handle the LLM call
# @app.route('/upload', methods=['POST'])
# async def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     if file:
#         filename = secure_filename(file.filename)
#         video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(video_path)
        
#         try:
#             # 1. Setup
#             prototype_script.setup_directories()
            
#             # 2. Extract Assets
#             audio_path = prototype_script.extract_audio(video_path)
#             frames = prototype_script.extract_keyframes(video_path, prototype_script.FRAME_INTERVAL_SECONDS)
            
#             # 3. Run AI Models
#             transcribed_data = []
#             if audio_path:
#                 transcribed_data = prototype_script.run_whisper_transcription(audio_path)
            
#             visual_captions = []
#             if frames:
#                 visual_captions = prototype_script.run_visual_analysis(frames)
            
#             # 4. Export Raw Data (Separate Files)
#             prototype_script.export_audio_data_to_text(transcribed_data)
#             prototype_script.export_visual_data_to_text(visual_captions)
            
#             # 5. Generate Final Study Guide using LLM (ASYNC CALL)
#             # This is where the magic happens!
#             study_guide_content = await asyncio.to_thread(
#                 prototype_script.generate_study_guide,
#                 prototype_script.AUDIO_TEXT_PATH,
#                 prototype_script.VISUAL_TEXT_PATH
#             )

#             # 6. Generate Merged Preview (The raw timeline)
#             timeline_preview_text = prototype_script.generate_web_preview(transcribed_data, visual_captions)

#             # 7. Return the study guide as the primary 'summary_preview' and the timeline as a secondary key.
#             # This ensures the study guide is displayed first, as requested by the user.
#             return jsonify({
#                 'success': True, 
#                 'timeline_preview': timeline_preview_text, # Retain the raw timeline
#                 'summary_preview': study_guide_content    # Study guide is now the main output
#             })

#         except Exception as e:
#             # Print error to console for debugging
#             print(f"Server Error: {e}")
#             return jsonify({'error': str(e)}), 500
    
#     return jsonify({'error': 'File type not allowed'}), 400

# if __name__ == '__main__':
#     # Flask needs an async event loop if using async def routes.
#     # We will let the environment handle the async execution when run with `app.run`.
#     app.run(debug=True, port=5000)

import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import prototype_script
import asyncio

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory dictionary to pass data between the API steps
session_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)
        
        # Initialize the session data for this specific file
        session_data[filename] = {'video_path': video_path}
        
        return jsonify({'success': True, 'filename': filename})
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/step1', methods=['POST'])
def step1():
    filename = request.json.get('filename')
    data = session_data.get(filename)
    try:
        prototype_script.setup_directories()
        data['audio_path'] = prototype_script.extract_audio(data['video_path'])
        data['frames'] = prototype_script.extract_keyframes(data['video_path'], prototype_script.FRAME_INTERVAL_SECONDS)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/step2', methods=['POST'])
def step2():
    filename = request.json.get('filename')
    data = session_data.get(filename)
    try:
        data['transcribed_data'] = prototype_script.run_whisper_transcription(data['audio_path'])
        prototype_script.export_audio_data_to_text(data['transcribed_data'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/step3', methods=['POST'])
def step3():
    filename = request.json.get('filename')
    data = session_data.get(filename)
    try:
        data['visual_captions'] = prototype_script.run_visual_analysis(data['frames'])
        prototype_script.export_visual_data_to_text(data['visual_captions'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/step4', methods=['POST'])
async def step4():
    filename = request.json.get('filename')
    data = session_data.get(filename)
    try:
        # Generate Final Study Guide using LLM
        study_guide_content = await asyncio.to_thread(
            prototype_script.generate_study_guide,
            prototype_script.AUDIO_TEXT_PATH,
            prototype_script.VISUAL_TEXT_PATH
        )

        # Generate Merged Preview
        timeline_preview_text = prototype_script.generate_web_preview(data['transcribed_data'], data['visual_captions'])
        
        # Clean up the session data now that we are done
        del session_data[filename]

        return jsonify({
            'success': True, 
            'timeline_preview': timeline_preview_text,
            'summary_preview': study_guide_content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)