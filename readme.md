
# Grader

This repository contains a Python script that performs code review on Java programs. It uses the OpenAI GPT-4 model to generate a detailed review of the code.

## Getting Started

To run the code review script, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/thisisamank/Grader.git
    ```

2. Install the required dependencies:
    ```bash
    pip install gitpython openai-async
    ```

3. Set up your OpenAI API key by replacing the `open_ai_key` variable in the script with your actual API key.

4. Run the script:
    ```bash
    python main.py
    ```

5. Enter the Git URL of the repository you want to review when prompted.

6. The script will clone the repository, process the Java files, generate a review, and save it as a Markdown file (`review.md`).

7. Optionally, you can convert the Markdown file to a PDF using Pandoc:
    ```bash
    pandoc review.md -o review.pdf --pdf-engine=xelatex -V geometry:"margin=0.5in"
    ```

## Example Output

The generated review will be in the format of a Markdown file and a PDF file (`review.pdf`).



