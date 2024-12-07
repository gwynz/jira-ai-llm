import requests
import json
mode = input("Enter 'r' for reading a URL or 's' for searching a query: ").strip().lower()

if mode == 'r':
    url = input("Enter the URL to read: ").strip()
    full_url = f"https://r.jina.ai/{url}"
    response = requests.get(full_url)
    with open("response.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
elif mode == 's':
    query = input("Enter the search query: ").strip()
    full_url = f"https://s.jina.ai/{query}"
    headers = {"Accept": "application/json"}
    response = requests.get(full_url, headers=headers)
    with open("response.json", "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4)
else:
    print("Invalid input. Please enter 'r' or 's'.")
