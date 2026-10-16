import base64

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

import config

IMAGE_PROMPT = "Describe this image in one sentence, including any visible labels or text."

TABLE_PROMPT = (
    "Summarize what this table shows in 1-2 short sentences: what kind of "
    "data it holds and any notable rows or values. Table (in markdown):\n\n"
)

def describe_image(image_path):
    """Ask the local vision model (config.VISION_MODEL) to describe an
    image file. Returns the description text, or None if it couldn't be
    generated."""
    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")

        llm = ChatOllama(model=config.VISION_MODEL, temperature=0)
        message = HumanMessage(
            content=[
                {"type": "text", "text": IMAGE_PROMPT},
                {"type": "image_url", "image_url": f"data:image/png;base64,{image_b64}"},
            ]
        )
        response = llm.invoke([message])
        return response.content.strip()
    except Exception as e:
        print(f"  (warning) could not describe image {image_path}: {e}")
        return None


def describe_table(markdown_table):
    """Ask the local text model (config.LLM_MODEL) to summarize a markdown
    table. Returns the summary text, or None if it couldn't be generated."""
    try:
        llm = ChatOllama(model=config.LLM_MODEL, temperature=0)
        response = llm.invoke(TABLE_PROMPT + markdown_table)
        return response.content.strip()
    except Exception as e:
        print(f"  (warning) could not describe table: {e}")
        return None
