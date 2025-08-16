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
        image,
    ])
    return response.text.strip()


def generate_from_text(title: str, keywords: str) -> str:
    if not title and not keywords:
        return "Please provide a title or keywords."
    prompt = (
        f"Create a detailed creative image prompt titled '{title}' using the keywords: {keywords}."
    )
    response = text_model.generate_content(prompt)
    return response.text.strip()


css = """
body {background-color:#1e1e1e;}
.gradio-container {background-color:#1e1e1e; color:#f5f5f5;}
textarea, input {background-color:#333; color:#f5f5f5;}
button {background-color:#4f46e5 !important; color:white !important; border-radius:6px;}
"""


with gr.Blocks(css=css, title="Prompt Master") as demo:
    gr.Markdown(
        "<h1 style='text-align:center;'>Prompt Master</h1>"
        "<p style='text-align:center;'>Generate prompts from images or text.</p>"
    )

    with gr.Tab("Image → Prompt"):
        with gr.Row():
            img = gr.Image(type="pil", label="Upload Image", height=512, width=512)
            img_prompt = gr.Textbox(label="Generated Prompt", lines=6)
        with gr.Row():
            img_btn = gr.Button("Generate & Copy", variant="primary")
            img_clear = gr.Button("Clear")
        img_btn.click(
            generate_from_image,
            inputs=img,
            outputs=img_prompt,
            js="(p)=>navigator.clipboard.writeText(p)",
        )
        img_clear.click(lambda: (None, ""), [], [img, img_prompt], queue=False)

    with gr.Tab("Text → Prompt"):
        with gr.Row():
            title = gr.Textbox(label="Title", placeholder="e.g. Sunset Mountain")
            keywords = gr.Textbox(label="Keywords", placeholder="comma separated")
        text_prompt = gr.Textbox(label="Generated Prompt", lines=6)
        with gr.Row():
            text_btn = gr.Button("Generate & Copy", variant="primary")
            text_clear = gr.Button("Clear")
        text_btn.click(
            generate_from_text,
            inputs=[title, keywords],
            outputs=text_prompt,
            js="(p)=>navigator.clipboard.writeText(p)",
        )
        text_clear.click(lambda: ("", "", ""), [], [title, keywords, text_prompt], queue=False)


if __name__ == "__main__":
    demo.launch(inbrowser=False)

