import openai
from openai import OpenAI, OpenAIError


def check_openai_api_key(api_key):

    try:
        client = OpenAI(
            api_key=api_key,
        )
        prompt = f"""
            what is your name?
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        return True
    except OpenAIError:
        return False
