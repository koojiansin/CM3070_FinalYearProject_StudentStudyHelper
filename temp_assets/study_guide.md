# CS50 with AI: A Study Guide

This guide summarizes key aspects of CS50's integration of AI, focusing on its pedagogical approach and practical applications.

## Introduction to CS50 and AI Policy

*   **Course Overview:** CS50 is Harvard University's introduction to computer science and the art of programming, also offered through the University of Oxford and via open courseware at [CS50.edx.org](https://cs50.edx.org).
*   **The Challenge of AI:** AI tools like ChatGPT are "all too helpful," often providing outright answers or code solutions, which can hinder the learning process in programming courses.
*   **CS50's AI Policy:**
    *   **Not Reasonable:** Using AI-based software (such as ChatGPT, Claude, Copilot, Gemini, Perplexity, et al.) that suggests or completes answers to questions or lines of code.
    *   **Reasonable:** Using CS50's own AI-based software, including the CS50 Duck (DDB) in [CS50.ai](https://cs50.ai) and [CS50.dev](https://cs50.dev).
*   **CS50's Approach:** The course built its own AI layer on top of underlying APIs from companies like OpenAI and Microsoft, imbuing it with a specific "personality" – that of a rubber duck.

## The CS50 Duck and Rubber Duck Debugging

*   **Concept of Rubber Duck Debugging:** A common practice in programming circles where one verbalizes their confusion or questions to an inanimate object (like a rubber duck). The act of verbalizing often leads to identifying the problem oneself, even if the duck doesn't respond.
*   **Evolution of the CS50 Duck:**
    *   **Pre-AI (Virtual Duck):** Initially, a virtual chat interface within CS50's programming environment would simply "quack" back pseudo-randomly (once, twice, or thrice) to a student's query. This alone anecdotally helped students by forcing them to articulate their problems.
    *   **Post-AI:** With the advent of large language model APIs (e.g., ChatGPT), the virtual duck began responding in English and other human languages, offering more direct (but guided) assistance.
    *   **Example Interaction (Pre-AI vs. Post-AI):**
        *   **Student:** "I'm hoping you can help me solve a problem."
        *   **DDB (Pre-AI):** "quack quack quack"
        *   **DDB (Post-AI):** "Of course, I'd be happy to help! Could you please provide more details about the problem you're facing?"

## Pedagogical Guardrails and Architecture

*   **Goal:** To implement "pedagogical guardrails" on top of AI APIs, making tools less "helpful" in the sense of providing direct answers, and more akin to a good teacher leading students to solutions.
*   **Aspiration:** Provide students with 24/7 "office hours" and approximate a 1:1 student-to-teacher (or student-to-duck) ratio.
*   **Architectural Components:**
    *   **CS50.ai:** A central web-based infrastructure.
    *   **APIs:** Integrates with Microsoft Azure and OpenAI.
    *   **Vector DB:** A local vector database used for Retrieval Augmented Generation (RAG) to ensure the duck's answers are precisely focused on CS50's course material.

## Scale and Acknowledgements

*   **Usage Statistics (as of lecture):**
    *   **Users:** 327,000 students and teachers globally.
    *   **Prompts:** Averaging 21,000 prompts/day.
    *   **Total Prompts:** 15.5 million so far.
*   **Special Thanks:** OpenAI, Microsoft, GitHub, and others.

## AI Features in CS50's Programming Environment

CS50 uses Visual Studio Code (VS Code) as its primary tool for writing code. [CS50.dev](https://cs50.dev) provides a cloud-based VS Code environment via GitHub Codespaces with pre-installed tools.

### 1. Explain Highlighted Code

*   **Functionality:** Students can highlight one or more lines of code in VS Code, right-click, and select "Explain Highlighted Code" from a custom plugin.
*   **Output:** The AI provides a ChatGPT-like explanation of the selected code.
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
    *   **Explanation:** "This code snippet is a simple C program that asks the user for their name and then greets them using their name. Let's break down the code step by step: 1. `#include <cs50.h>`: This line includes the "cs50.h" header file... 2. `#include <stdio.h>`: This line includes the "stdio.h" header file... 3. `int main(void)`: This line defines the main function of the program..."

### 2. Improve Code Style (Style50)

*   **Purpose:** Advise students on improving the aesthetics and formatting of their code without automatically fixing it initially.
*   **Functionality:** Students can click a "Style50" button to see their code at left and the ideal, style-guide-compliant version at right, with red and green highlights indicating necessary additions or subtractions.
*   **"Explain Changes" Feature:** Students can click "Explain Changes" to receive an AI-generated explanation of *how* and *why* to make the stylistic adjustments.
*   **"Apply Changes" Feature:** Once muscle memory is developed, students can automatically apply the suggested style changes.
*   **Example (C code formatting):**
    ```c
    // Original (poorly formatted)
    #include<stdio.h>
    int main(void)
    {
    for(int i=0; i<3; i++)
    {
    printf ("meow\n");
    }
    }

    // Ideal (right pane of Style50)
    #include <stdio.h>
    int main(void)
    {
        for (int i = 0; i < 3; i++)
        {
            printf("meow\n");
        }
    }
    ```
    *   **Explanation of Changes (excerpt):** "The changes are made at line 1 and lines 5 to 8 in the file. At line 1, the change is in the inclusion of the header. It was originally written as `#include<stdio.h>` but it has been modified to `#include <stdio.h>`. At lines 5 to 8, the changes are in the formatting of a for loop..."

### 3. Improve Code Design (Design50)

*   **Purpose:** Advise students on improving the overall design, efficiency, readability, and maintainability of their code – akin to a code review.
*   **Functionality:** Students click a "Design50" button. Even with correct code, the AI provides a ChatGPT-like explanation of how to improve its design.
*   **Example (Python `mario.py`):**
    *   **Design Feedback (excerpt):** "The code has several design inefficiencies and unnecessary complexities. Here are some high-level feedback points:
        1.  **Input Handling:** The input validation loop is overly complex. Simplifying this would make the code more readable and maintainable.
        2.  **Variable Usage:** The use of multiple variables like `counter` and `output_string` can be streamlined to reduce clutter.
        3.  **Loop Logic:** The nested loops for constructing the output string are convoluted..."

## CS50.AI: Direct Duck Interface

*   **Functionality:** Students can directly visit [CS50.ai](https://cs50.ai) to ask questions and copy-paste code outside of VS Code.
*   **Disclaimer:** A prominent disclaimer reminds students to "think critically" as AI can "hallucinate or really make things up."
*   **Pedagogical Aim:** The duck aims to lead students to solutions by asking guiding questions and providing minimal lines of code, rather than outright answers.
*   **Example Interaction:**
    *   **Student:**
        ```python
        x = input("Give me an integer x: ")
        y = input("Give me an integer y: ")
        sum = x+y
        print("x + y is: " + sum)
        ```
        "My code is not working as expected, any ideas?"
    *   **DDB:** "It seems like you're trying to add two integers, but the `input()` function in Python returns a string. So, when you try to add `x` and `y`, you're actually concatenating two strings, not adding two integers. To fix this, you can convert the inputs to integers using the `int()` function like so:
        ```python
        x = int(input("Give me an integer x: "))
        y = int(input("Give me an integer y: "))
        ```

## System Prompt: AI's Behavioral Guidelines

The underlying AI APIs receive a "system prompt" — English-like instructions on how to behave for CS50 users.

*   **Example System Prompt:**
    ```
    You are a friendly and supportive teaching assistant for CS50.
    You are also a rubber duck.
    Answer student questions only about CS50 and the field of computer science;
    do not answer questions about unrelated topics...
    Do not provide full answers to problem sets, as this would violate academic honesty...
    Answer this question:
    ```
    (This is followed by the "user prompt," which is the student's actual question.)

## Impact of AI Tools

The introduction of these AI tools has had an immediate and significant impact:

*   **Impact on TAs:**
    *   **Without AI:** Students asked an average of 0.89 questions each of TAs.
    *   **With AI:** Students asked an average of 0.28 questions each of TAs. Students now prefer asking questions of the virtual duck.
*   **Impact on Office Hours:**
    *   **Without AI:** Students attended 51% of available office hours.
    *   **With AI:** Students attended 30% of available office hours.
*   **Impact on Assessments:** Grades are improving, leading to questions about distinguishing student capabilities. This is likely due to the continuous, iterative feedback provided by the AI throughout the week.
*   **Future Direction: Oral Examinations:** CS50 is experimenting with digital, adaptive oral examinations where the duck dynamically questions students about course material to provide individualized assessments of strengths and weaknesses.

## Student Feedback

A favorite quote from initial evaluations:

> "It felt like having a personal tutor. I love how AI bots will answer questions without ego and without judgment, generally entertaining even the stupidest of questions without treating them like they're stupid. It has an, as one could expect, inhuman level of patience."

## Further Reading

For more in-depth information on CS50's AI integration:

*   **"Teaching CS50 with AI"** (ACM SIGCSE)
*   **"Improving AI in CS50"** (Follow-on paper)

All links and papers can be accessed via the QR code mentioned in the lecture.