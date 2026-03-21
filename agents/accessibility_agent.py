from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def accessibility_agent(explanation: str):
    prompt = f"""
Convert this into a screen-reader friendly explanation.
Use spatial and step-by-step descriptions.

{explanation}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output[0].content[0].text