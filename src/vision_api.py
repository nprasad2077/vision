from dotenv import load_dotenv
import os
import openai
import base64
import requests

# Load environment variables from the .env file
load_dotenv()
api_key = os.getenv("KEY")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_image(image_path):
    base64_image = encode_image(image_path)
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    structured_prompt = """Analyze the image and provide a structured description of the main item in the following format:

1. Name: [Single word name of the main item]
2. Type: [Single word type or category of the item]
3. Colors: [List the prominent colors, separated by commas]
4. Size: [Estimate the size if possible: small, medium, large, or unknown]
5. Condition: [Describe the condition if apparent: new, used, damaged, etc.]
6. Features: [List notable features or characteristics, separated by commas]
7. Setting: [Describe the setting or background if relevant]
8. Associated Items: [List any associated items or objects in the image, separated by commas]
9. Brand: [Mention the brand if identifiable]
10. Character: [If the item represents a character, name the character]

Please provide a detailed description of the item, focusing on visual attributes that can be easily identified and categorized. Use simple, descriptive language and avoid complex sentences."""

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": structured_prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 500,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    data = response.json()

    print(data["choices"][0]["message"]["content"])
    return data["choices"][0]["message"]["content"]
