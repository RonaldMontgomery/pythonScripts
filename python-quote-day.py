# https://python.plainenglish.io/5-beginner-python-projects-that-actually-teach-you-how-to-think-like-a-coder-a2f4e102b8b3
import requests

def get_quote():
    response = requests.get("https://zenquotes.io/api/today")
    data = response.json()  # a list with one dict
    quote = data[0]["q"]
    author = data[0]["a"]
    print(f'"{quote}" — {author}')

get_quote()