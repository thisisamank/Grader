from git import Repo
import os
from openai import AsyncOpenAI
import asyncio


open_ai_key = ""


def gpt_prompt(code: str, file_name: str):
    return f"""
You are a very strict computer science professor teaching Java to freshers. You have given assignments to your students to write a Java program to solve a particular problem. You have received the following code from one of your students. You always point out the both the pros and cons but empasize on cons so that the student can improve. Also judge on file name if that is adhering to the standards.

The review should include the following points:
 - The code is well-written and easy to understand.
 - Follows best practices, Java conventions and coding standards.
 - The code is efficient and optimized.

 Your review should be in bullet points.

The code provided by the student is:
{code}

The filename is: {file_name}

Start the review by marking each program out of 10. Then provide a detailed review of the code with where did you cut the marks and why.
Your output should be in the format of a markdown. The output should not exceed 100 words and should be concise and to the point. We don't need your introduction or conclusion. Just the review of the code with pros and cons.

Format of the output:
 ** Marks scored: __/10 **

 ** Pros: **
 
 ** Cons (with marks deducted and reason):**
    """


async def process_files_in_directory(directory: str):
    review_of_code = f"""
    ## Code Review

<div style="page-break-after: always;"></div>

    """
    os.walk(directory)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                with open(os.path.join(root, file), "r") as f:
                    code = f.read()
                    review_of_code = review_of_code + \
                        await review_code_from_gpt(code, file)

    str_to_markdown_file(review_of_code, "review.md")
    markdown_to_pdf("review")


client = AsyncOpenAI(
    api_key=open_ai_key
)


async def review_code_from_gpt(code: str, file_name: str):
    prompt = gpt_prompt(code, file_name)

    output_from_gpt = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
    )

    response = f"""

### {file_name}

Your code was:

```java
{code}
```
Here is the review of your code:
{output_from_gpt.choices[0].message.content}

"""
    print(response)
    return response


def str_to_markdown_file(content: str, file_name: str):
    with open(file_name, "w") as f:
        f.write(content)


def markdown_to_pdf(file_name: str):
    os.system(
        f'pandoc review.md -o review.pdf --pdf-engine=xelatex -V geometry:"margin=0.5in"')


async def main():
    git_url = input("Enter the git url: ")
    Repo.clone_from(git_url, "repo")
    await process_files_in_directory("repo")
    os.system("rm -rf repo")


if __name__ == "__main__":
    asyncio.run(main())
