import os
import requests

def get_chatbot_response(userinput):
    api_key = ""
    URL2 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": userinput}]
        }],
    }
    
    try:
        response2 = requests.post(URL2, json=payload).json()
        text_output = response2["candidates"][0]["content"]["parts"][0]["text"]
        return text_output
    except Exception as e:
        return f"Error retrieving response: {e}"

if __name__ == "__main__":
    userinput = input("please enter your question: ")
    print(get_chatbot_response(userinput))
