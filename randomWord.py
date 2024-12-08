import requests

# API endpoint
url = "https://random-word-api.herokuapp.com/word"

response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # grab the random word from the response JSON
    word = response.json()[0]  # the result is a list of words, so we access the first element
    print(f"Random word: {word}")
else:
    print(f"Error: {response.status_code}")
