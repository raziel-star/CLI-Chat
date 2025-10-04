import os
from google import genai
from utils import extract_text

def create_file(filename, content):
    full_path = os.path.abspath(filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return full_path

def generate_feedback(filename, content, client):
    prompt = (
        f"You are CLI-Chat, a professional AI assistant.\n"
        f"A file named '{filename}' was created with the following content:\n"
        f"{content}\n"
        "Provide concise, professional feedback on the content. Do not rewrite it."
    )
    try:
        response = client.models.generate_content(model="gemini-2.5-pro", contents=[prompt])
        return extract_text(response)
    except Exception as e:
        return f"Error generating feedback: {e}"

