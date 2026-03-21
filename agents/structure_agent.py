from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def structure_agent(description: str):
    prompt = f"""
Convert the following into structured STEM data:
{description}

Return JSON with:
- type
- key elements
- relationships
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output[0].content[0].text