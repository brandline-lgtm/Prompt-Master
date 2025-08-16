import os
import gradio as gr
import google.generativeai as genai
from PIL import Image

# Configure the Gemini API using the provided key
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBcyITJfGQ5Bs61WNLEKBKyCJQ8ITNRL0A")
genai.configure(api_key=API_KEY)

# Models
text_model = genai.GenerativeModel("gemini-pro")
image_model = genai.GenerativeModel("gemini-pro-vision")

def generate_from_image(image: Image.Image) -> str:
    if image is None:
        return "Please upload an image."
    response = image_model.generate_content([
        "Create a concise creative prompt that could be used to reproduce a similar image:",
        image
    ])
    return response.text.strip()

def generate_from_text(title: str, keywords: str) -> str:
    if not title and not keywords:
        return "Please provide a title or keywords."
    prompt = f"Create a detailed creative image prompt titled '{title}' using the keywords: {keywords}."
    response = text_model.generate_content(prompt)
    return response.text.strip()

css = """
body {background-color: #1e1e1e;}
.gradio-container {background-color: #1e1e1e; color: #f5f5f5;}
textarea, input {background-color:#333; color:#f5f5f5;}
button {background-color:#4f46e5 !important; color:white !important;}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("# Prompt Master")
    with gr.Tab("From Image"):
        img = gr.Image(type="pil", label="Upload Image")
        img_prompt = gr.Textbox(label="Generated Prompt", lines=4)
        img_btn = gr.Button("Generate & Copy")
        img_btn.click(
            generate_from_image,
            inputs=img,
            outputs=img_prompt,
            js="(p)=>navigator.clipboard.writeText(p)"
        )
    with gr.Tab("From Title/Keywords"):
        title = gr.Textbox(label="Title")
        keywords = gr.Textbox(label="Keywords (comma separated)")
        text_prompt = gr.Textbox(label="Generated Prompt", lines=4)
        text_btn = gr.Button("Generate & Copy")
        text_btn.click(
            generate_from_text,
            inputs=[title, keywords],
            outputs=text_prompt,
            js="(p)=>navigator.clipboard.writeText(p)"
        )

if __name__ == "__main__":
    demo.launch()
