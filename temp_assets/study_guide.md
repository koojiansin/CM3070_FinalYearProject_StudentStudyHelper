# CS50 with AI: A Study Guide

## 1. Introduction to CS50 and AI Policy

*   **What is CS50?**
    *   Harvard University's introduction to computer science and programming.
    *   Also offered through the University of Oxford and as open courseware (free online).
    *   Can be accessed at [cs50.edx.org](http://cs50.edx.org)
*   **Initial Policy on AI (ChatGPT et al.):**
    *   **Not Reasonable:** Using AI-based software (such as ChatGPT, Claude, Copilot, Gemini, Perplexity, etc.) that suggests or completes answers to questions or lines of code. This would violate academic honesty and hinder learning.
    *   **Reasonable:** Using CS50's own AI-based software, including the CS50 Duck (DDB) in [cs50.ai](http://cs50.ai) and [cs50.dev](http://cs50.dev).
*   **Motivation for CS50's AI:** To leverage nascent AI technology while maintaining pedagogical integrity, building a custom layer on top of APIs from companies like OpenAI and Microsoft.

## 2. The CS50 Duck and Rubber Duck Debugging

*   **Concept of Rubber Duck Debugging:**
    *   A common practice in programming.
    *   Verbalizing confusion or questions to an inanimate object (like a rubber duck) on your desk.
    *   The act of verbalization often clarifies thoughts and helps realize logical flaws, even if the "duck" doesn't respond.
*   **Evolution of CS50's Virtual Duck:**
    *   **Pre-AI (Virtual Duck Debugger):** Implemented virtually in CS50's programming environment even before modern AI. When students typed questions, the virtual duck would respond with "quack quack quack" (pseudo-randomly one, two, or three times). Anecdotal evidence suggests this alone helped students unblock themselves by forcing them to verbalize their thoughts.
    *   **Post-AI:** With the advent of ChatGPT and underlying APIs, the virtual duck began responding literally in English (and other human languages), transforming into an intelligent tutor.

## 3. Pedagogical Guardrails and Goals

*   **Objective:** Implement "pedagogical guardrails" on top of underlying AI APIs.
*   **Purpose:**
    *   Make tools like ChatGPT *less helpful* in terms of providing direct answers.
    *   Guide students to solutions, akin to a good teacher, rather than providing outright answers.
    *   Approximate a 1:1 student-to-teacher (or student-to-duck) ratio.
*   **Overall Goal:** Provide students with 24/7 "office hours" for one-on-one support.

## 4. Architectural Overview of CS50.ai

*   **Central Infrastructure:** [cs50.ai](http://cs50.ai) (a web address and feature channel).
*   **API Integration:** Communicates with APIs from Microsoft Azure and OpenAI.
*   **Local Vector Database:**
    *   Used for Retrieval Augmented Generation (RAG).
    *   Queries a local database to focus the duck's answers precisely on CS50 course material.

## 5. Scale and Impact

*   **Deployment:** Deployed at Harvard and to hundreds of thousands of students and teachers worldwide.
*   **Usage Statistics (as of lecture date):**
    *   **Users:** 327,000 students and teachers.
    *   **Prompts:** Averaging 21,000 prompts/questions per day.
    *   **Total Prompts:** 15.5 million so far.
*   **Acknowledgements:** Thanks to OpenAI, Microsoft, GitHub, and others.

## 6. CS50's Programming Environment: VS Code for CS50

*   **Tool:** Visual Studio Code (VS Code), a popular open-source product from Microsoft.
*   **Access:**
    *   Can be downloaded on personal Macs/PCs.
    *   Accessible in the cloud via GitHub Codespaces at [cs50.dev](http://cs50.dev).
*   **Benefits of CS50.dev:** Pre-installs necessary software, reducing technical headaches for students at the start of the semester. Students can eventually download their work to their local machines.

## 7. AI-Powered Features in VS Code for CS50

### 7.1. Explain Highlighted Code

*   **Functionality:** A custom plugin for VS Code.
*   **Usage:** Students highlight one or more lines of code, right-click (or control-click), and select "Explain Highlighted Code."
*   **Output:** A ChatGPT-like explanation appears, breaking down the code step-by-step, similar to what a teacher would provide.

    *   **Example (C code):**
        ```c
        #include <cs50.h>
        #include <stdio.h>

        int main(void)
        {
            string name = get_string("What is your name? ");
            printf("hello, %s\n", name);
        }
        ```
    *   **Explanation Output (excerpt):**
        > This code snippet is a simple C program that asks the user for their name and then greets them using their name. Let's break down the code step by step:
        > 1. `#include <cs50.h>`: This line includes the "cs50.h" header file...
        > 2. `#include <stdio.h>`: This line includes the "stdio.h" header file...
        > 3. `int main(void)`: This line defines the main function...

### 7.2. Style 50

*   **Functionality:** Advises students on how to improve their code style (aesthetics, formatting) without automatically fixing it initially.
*   **Usage:**
    *   Students click a "Style 50" button.
    *   A side-by-side comparison shows their code (left) and the ideal formatted version (right), with red/green highlights indicating changes.
*   **"Explain Changes" Feature:** Students can click "Explain Changes" to get a ChatGPT-like explanation of *how* and *why* they should make the suggested style improvements.
*   **"Apply Changes" Feature:** Once muscle memory is developed, students can click "Apply Changes" to automatically format their code.

    *   **Example (Poorly formatted C code):**
        ```c
        #include<stdio.h>
        int main(void)
        {
        for(int i=0; i<3; i++)
        {
        printf("meow\n");
        }
        }
        ```
    *   **Explanation Output (excerpt):**
        > The changes are made at line 1 and lines 5 to 8 in the file. At line 1, the change is in the inclusion of the header. It was originally written as `#include<stdio.h>` but has been modified to `#include <stdio.h>`. At lines 5 to 8, the changes are in the formatting of a for loop. It was originally written as:
        > `for(int i=0; i<3; i++) { printf("meow\n"); }`
        > But it has been modified to:
        > `for(int i=0; i<3; i++) { printf("meow\n"); }`

### 7.3. Design 50

*   **Functionality:** Advises students on how to improve their code's *design* (efficiency, readability, maintainability), even if it's functionally correct. This was traditionally reliant on human TAs.
*   **Usage:** Students click a "Design 50" button.
*   **Output:** Provides a ChatGPT-like explanation and high-level feedback, similar to a code review, to make code more maintainable, readable, and well-designed.

    *   **Example (Python code):**
        ```python
        def mario():
            x = input("Give me an integer x: ")
            while not x.isdigit() or int(x) < 1 or int(x) > 8:
                print("Please enter a number between 1 and 8:")
                x = input()
            # Parsing user input multiple times unnecessarily
            height = int(x)
            # Setting up unnecessary variables
            counter = 0
            output_string = ""
            # Loop through each row
            while counter < height:
                # Convoluted logic to print spaces
                for i in range(height - counter - 1):
                    output_string += " "
                # Even more convoluted logic to print hashes
                for j in range(counter + 1):
                    output_string += "#"
                # Weird way to add a new line
                output_string += "\n"
                counter += 1
            print(output_string)
        ```
    *   **Design Feedback (excerpt):**
        > The code has several design inefficiencies and unnecessary complexities. Here are some high-level feedback points:
        > 1.  **Input Handling:** The input validation loop is overly complex. Simplifying this would make the code more readable and maintainable.
        > 2.  **Variable Usage:** The use of multiple variables like `counter` and `output_string` can be streamlined to reduce clutter.
        > 3.  **Loop Logic:** The nested loops for constructing the output string are convoluted. Simplifying the logic for generating the output string would improve clarity.

## 8. CS50.ai Web Interface

*   **Functionality:** A direct web interface for students to ask questions and copy-paste code.
*   **Disclaimer:** Includes a disclaimer reminding students to think critically, as AI can "hallucinate" or make things up.
*   **Pedagogical Approach:** The AI provides teacher-like explanations, often with minimal code, generally leading students to a solution rather than providing it outright.

    *   **Example Interaction:**
        *   **Student:** `My code is not working as expected, any ideas? x = input("Give me an integer x: ") y = input("Give me an integer y: ") sum = x+y print("x + y is: " + sum)`
        *   **Duck:** `It seems like you're trying to add two integers, but the input() function in Python returns a string. So, when you try to add x and y, you're actually concatenating two strings, not adding two integers. To fix this, you can convert the inputs to integers using the int() function like so: x = int(input("Give me an integer x: ")) y = int(input("Give me an integer y: "))`

## 9. System Prompt: Guiding the AI

*   **Mechanism:** CS50 guides the underlying AI APIs using a "system prompt" – English-like instructions on how the AI should behave.
*   **Example System Prompt (Simplified):**
    ```
    You are a friendly and supportive teaching assistant for CS50.
    You are also a rubber duck.
    Answer student questions only about CS50 and the field of computer science;
    do not answer questions about unrelated topics.
    Do not provide full answers to problem sets, as this would violate academic honesty.
    Answer this question: [User's question is appended here]
    ```

## 10. Impact of AI Tools on Learning and Teaching

*   **Impact on TA Questions:**
    *   **Without AI:** Students asked an average of **0.89 questions each** of TAs.
    *   **With AI:** Students asked an average of **0.28 questions each** of TAs, preferring the virtual duck.
*   **Impact on Office Hours Attendance:**
    *   **Without AI:** Students attended **51%** of available office hours.
    *   **With AI:** Students attended **30%** of available office hours.
*   **Impact on Assessments:**
    *   Grades are generally improving, posing questions about assessment design (distinguishing student work).
    *   Iterative feedback from AI tools throughout the week likely contributes to higher quality submissions.
*   **Future Directions (Near-Term):** Experimenting with digital oral examinations where the duck dynamically asks adaptive questions to assess student strengths and weaknesses.

## 11. Student Feedback

*   **Quote:** "It felt like having a personal tutor. I love how AI bots will answer questions without ego and without judgment, generally entertaining even the stupidest of questions without treating them like they're stupid. It has an, as one could expect, inhuman level of patience."

## 12. Further Reading

*   **Academic Papers:**
    *   "Teaching CS50 with AI" (ACM SIGCSE)
    *   "Improving AI in CS50" (Follow-on paper)
*   **Resources:** Papers and links can be found via a QR code (presented at the end of the lecture).