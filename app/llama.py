import subprocess
import tempfile
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("MODEL_NAME")

async def generate_summary(text: str) -> str:
    prompt = f"Summarize the following book content in just 4-5 lines:\n\n{text}"
    return await run_llama(prompt)

async def generate_review_summary(reviews: List) -> str:
    review_texts = "\n\n".join([r.review_text for r in reviews])
    prompt = f"Summarize the following user reviews:\n\n{review_texts}"
    return await run_llama(prompt)

async def run_llama(prompt: str) -> str:
    try:
        # Write the prompt to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as f:
            f.write(prompt)
            file_path = f.name

        # Run LLaMA 3 using Ollama and redirect input from the file
        result = subprocess.run(
            f"type \"{file_path}\" | ollama run {model_name}",
            capture_output=True,
            text=True,
            shell=True
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"[LLM Error] Failed to generate summary: {result.stderr}"

    except Exception as e:
        return f"[LLM Error] {str(e)}"
