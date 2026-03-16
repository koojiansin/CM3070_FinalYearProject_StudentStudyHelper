# CS50 with AI: A Study Guide

## 1. Introduction to CS50 and AI Policy

*   **Course Overview:** CS50 is Harvard University's introduction to computer science and programming. It's also offered through the University of Oxford and via open courseware for free online.
*   **Access CS50:** Visit [cs50.edx.org](https://cs50.edx.org) to start the course.
*   **AI Policy (Not Reasonable):**
    *   AI-based tools like ChatGPT, Claude, Copilot, Gemini, Perplexity, etc., are **not reasonable** for suggesting or completing answers to questions or lines of code. These tools have become "all too helpful, all too willing to answer a student's question outright, or even provide outright solutions to code."
    *   This policy was decreed early in the course syllabus.

## 2. CS50's Own AI-based Software: The CS50 Duck

*   **CS50's Approach (Reasonable):**
    *   Using CS50's own AI-based software is **reasonable**.
    *   This includes the **CS50 Duck (DDB)**, available in **cs50.ai** and **cs50.dev**.
*   **Leveraging AI:** CS50 built its own layer on top of underlying APIs from companies like OpenAI and Microsoft to incorporate a "personality" in the form of a rubber duck.
*   **Goals:**
    *   Implement **pedagogical guardrails** to make AI tools "less helpful" in terms of providing direct answers.
    *   Behave like a good teacher, leading students to solutions rather than providing answers outright.
    *   Provide students with 24/7 "office hours" for one-on-one support.
    *   Approximate a **1:1 student-to-duck ratio**.

## 3. The Concept of Rubber Duck Debugging

*   **Definition:** A common programming practice where you verbalize your confusion or questions to an inanimate object (like a rubber duck) on your desk.
*   **Purpose:** The act of verbalizing often helps clarify thoughts, leading to a "proverbial light bulb" moment, even if the duck doesn't respond. This helps realize "the illogic in your thoughts."

## 4. Evolution of the CS50 Duck Debugger

*   **Pre-AI Era (Virtual Duck):**
    *   Implemented virtually within CS50's programming environment even before AI's prevalence.
    *   Initially, if a student typed a question like "I'm hoping you can help me solve a problem," the virtual duck would "quack back" (e.g., "ddb quack quack quack") one to three times pseudo-randomly.
    *   Anecdotal evidence showed this was sufficient to unblock students, as the act of typing out their confusion helped them.
*   **Post-AI Era:**
    *   With the advent of ChatGPT and underlying APIs, the same virtual duck started "literally responding to students in English" (or other human languages) overnight.
    *   Example response: "Of course, I'd be happy to help! Could you please provide more details about the problem you're facing?"

## 5. Architectural Overview

*   **Central Infrastructure:** **CS50.ai** serves as the central web-based infrastructure and channel for all features.
*   **API Integration:** Communicates with APIs from Microsoft Azure and OpenAI.
*   **Vector Database (RAG):** Utilizes a local vector database to implement Retrieval Augmented Generation (RAG). This allows querying CS50's own database to focus the duck's answers precisely on course material.

## 6. Scale and Impact

*   **Deployment:** Deployed at Harvard and to hundreds of thousands of students and teachers worldwide.
*   **Usage Statistics (as of lecture date):**
    *   **327,000 users** (students and teachers)
    *   **21,000 prompts/day** on average
    *   **15.5 million total prompts** so far

## 7. CS50.dev and Visual Studio Code Integration

*   **Primary Coding Tool:** Visual Studio Code (VS Code) is used by students to write code. It's a popular, largely open-source product from Microsoft.
*   **CS50.dev:** Students log into **cs50.dev**, a web-based interface that provides a pre-configured VS Code environment via GitHub Codespaces.
    *   This pre-installs necessary tools, reducing "start of semester technical support headaches."
    *   Students are encouraged to download VS Code onto their own machines by the end of the semester.

## 8. AI Features in VS Code

CS50 developed a plugin for VS Code to provide AI-powered assistance:

### A. Explain Highlighted Code

*   **Functionality:** Students can highlight one or more lines of code in a file (e.g., a C file like `hello.c`).
*   **Usage:** Right-click (or Control-click) and select **"Explain Highlighted Code"**.
*   **Output:** A ChatGPT-like explanation of the selected code appears, akin to a teacher walking students through it.
    *   Example: For `hello.c`, an explanation would detail `#include <cs50.h>`, `#include <stdio.h>`, `int main(void)`, `string name = get_string(...)`, and `printf(...)`.

### B. Style50 (Code Style Improvement)

*   **Functionality:** Advises students on how to improve code aesthetics and formatting without automatically fixing it.
*   **Usage:** Click the **"Style50"** button (top right).
*   **Output:** Shows a side-by-side comparison: student's code on the left, ideally formatted code on the right (based on a style guide). Red and green highlights indicate additions/subtractions needed.
*   **Explanation:** Students can click **"Explain Changes"** for a ChatGPT-like explanation of *how* and *why* to make the changes.
    *   Example: Explains how an `#include` statement might be formatted differently or how a `for` loop's indentation should be adjusted.
*   **Automation:** Once muscle memory is developed, students can click **"Apply Changes"** to automatically reformat the code.

### C. Design50 (Code Design Improvement)

*   **Functionality:** Advises students on how to improve code design (correctness, efficiency, readability, maintainability), a task traditionally reliant on human TAs or code reviews.
*   **Usage:** Click the **"Design50"** button.
*   **Output:** Provides a ChatGPT-like explanation of how to improve the code, even if it's already working correctly.
    *   Example for `mario.py`: Identifies "design inefficiencies and unnecessary complexities," offering high-level feedback on:
        1.  **Input Handling:** Suggests simplifying overly complex input validation loops.
        2.  **Variable Usage:** Advises streamlining multiple unnecessary variables.
        3.  **Loop Logic:** Points out convoluted nested loops for constructing output strings.

## 9. CS50.ai Direct Interface

*   **Functionality:** Allows students to ask general questions and copy-paste code that might not be in the VS Code window.
*   **Disclaimer:** A disclaimer reminds students to "think critically" as AI can "hallucinate or really make things up."
*   **Output:** Provides teacher-like explanations, minimal lines of code (if any), generally leading students to a solution rather than providing it outright.
    *   **Example Interaction:**
        *   **Student:** "My code is not working as expected, any ideas? `x = input('Give me an integer x: ')`, `y = input('Give me an integer y: ')`, `sum = x+y`, `print('x + y is: ' + sum)`"
        *   **Duck:** Explains that `input()` returns a string, leading to concatenation instead of addition, and suggests converting inputs to integers using `int()`.
            ```python
            x = int(input("Give me an integer x: "))
            y = int(input("Give me an integer y: "))
            ```

## 10. System Prompt: Guiding the AI

*   **Core Concept:** Underlying APIs are given a "system prompt" – English-like instructions on how to behave.
*   **CS50's System Prompt (Simplified):**
    ```
    You are a friendly and supportive teaching assistant for CS50.
    You are also a rubber duck.
    Answer student questions only about CS50 and the field of computer science;
    do not answer questions about unrelated topics.
    Do not provide full answers to problem sets, as this would violate academic honesty.
    Answer this question:
    ```
*   **User Prompt:** The student's question is then appended to this system prompt.

## 11. Impact on Teaching and Learning Metrics

*   **Impact on TAs:**
    *   **Without AI:** Students asked an average of **0.89 questions each** of TAs.
    *   **With AI:** Students asked an average of **0.28 questions each** of TAs, preferring the virtual duck.
*   **Impact on Office Hours:**
    *   **Without AI:** Students attended **51%** of available office hours.
    *   **With AI:** Students attended only **30%** of available office hours.
*   **Impact on Assessments:**
    *   Grades are increasing, raising questions about what exactly is being assessed.
    *   This is partly due to students receiving "iterative feedback throughout the week" from the AI, leading to better submissions.
*   **Near-term Experimentation:** Resurrection of "yesterday's oral examinations," digitally implemented. The duck dynamically and adaptively asks questions about material to provide individualized assessments of strengths and weaknesses.

## 12. Student Feedback

*   **Favorite Quote:** "It felt like having a personal tutor."
*   **Key Benefits of AI Bots:**
    *   Answer questions without ego and without judgment.
    *   Entertain even "the stupidest of questions" without treating them as such.
    *   Possess an "inhuman level of patience."

## 13. Further Reading

*   **Papers:**
    *   "Teaching CS50 with AI" (ACM SIGCSE)
    *   "Improving AI in CS50" (Follow-on paper)
*   **Access:** Papers and all related links can be found via a provided QR code.