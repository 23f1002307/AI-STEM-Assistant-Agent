from openai import OpenAI
from config import OPENAI_API_KEY
import base64

client = OpenAI(api_key=OPENAI_API_KEY)

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def vision_agent(image_path: str):
    base64_image = encode_image(image_path)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Describe this STEM image in a structured and educational way."
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image}"
                    }
                ]
            }
        ]
    )

    return response.output[0].content[0].text