from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def chat_agent(question: str, context: dict):
    prompt = f"""
You are a STEM tutor helping a visually impaired student.

Context:
Description: {context['description']}
Structured: {context['structured']}
Explanation: {context['final_output']}

Question:
{question}

Answer clearly and accessibly.
Format the output in a proper semantic manner so that navigating through the information becomes easier with screen readers.
Use semantic structure for headings, lists, and other elements to make the generated explanation screen reader friendly.

"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output[0].content[0].text