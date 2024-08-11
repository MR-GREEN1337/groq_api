import os
from groq import Groq
import requests


async def get_models():
    api_key = os.environ.get("GROQ_API_KEY")
    # Check if the API key is loaded
    if not api_key:
        raise ValueError("API key is not set. Please check your .env file.")

    # print(f"API Key: {api_key}")  # Print API key to verify it's loaded correctly

    url = "https://api.groq.com/openai/v1/models"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    response = requests.get(url, headers=headers)

    response = response.json()
    models = [
        model["id"]
        for model in response["data"]
        if (
            "llama" in model["id"] or "mixtral" in model["id"] or "gemma" in model["id"]
        )
    ]

    return models


async def inference_model(prompt: str, model_name: str):
    client = Groq(
        # This is the default and can be omitted
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "you are a helpful assistant."},
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model=model_name,
    )

    # print(chat_completion.choices[0].message.content)

    return chat_completion.choices[0].message.content


"""if __name__ == "__main__":
    result = asyncio.run(
        inference_model(prompt="1+1?", model_name="llama-3.1-8b-instant")
    )
    print(result)"""
