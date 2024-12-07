import requests
import json

def get_headers():
    headers = {}
    api_key = input("Enter your Jina API key (or leave blank to skip): ").strip()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    options = [
        "1. Image Caption - Captions all images at the specified URL.",
        "2. Gather All Links At the End - Creates a 'Buttons & Links' section at the end.",
        "3. Gather All Images At the End - Creates an 'Images' section at the end.",
        "4. JSON Response - Returns the response in JSON format.",
        "5. Forward Cookie - Forwards your custom cookie settings.",
        "6. Use a Proxy Server - Utilizes your proxy to access URLs.",
        "7. Bypass the Cache - Bypasses the API server cache.",
        "8. Stream Mode - Allows more time for the page to fully render.",
        "9. Target Selector - Focuses on a specific part of the page using a CSS selector.",
        "10. Custom Timeout - Sets a custom timeout for the request.",
        "11. Wait For Selector - Waits for a specific element to appear before returning.",
        "12. Level of Details - Controls the level of detail in the response."
    ]
    
    print("Choose options by entering their numbers, separated by commas:")
    for option in options:
        print(option)
    
    choices = input("Enter your choices or leave blank to skip: ").strip().split(',')
    for choice in choices:
        choice = choice.strip()
        if choice == '1':
            headers["X-With-Generated-Alt"] = "true"
        elif choice == '2':
            headers["X-With-Links-Summary"] = "true"
        elif choice == '3':
            headers["X-With-Images-Summary"] = "true"
        elif choice == '4':
            headers["Accept"] = "application/json"
        elif choice == '5':
            cookie = input("Enter your cookie settings: ").strip()
            headers["X-Set-Cookie"] = cookie
        elif choice == '6':
            proxy = input("Enter your proxy URL: ").strip()
            headers["X-Proxy-Url"] = proxy
        elif choice == '7':
            headers["X-No-Cache"] = "true"
        elif choice == '8':
            headers["Accept"] = "text/event-stream"
        elif choice == '9':
            selector = input("Enter the CSS selector: ").strip()
            headers["X-Target-Selector"] = selector
        elif choice == '10':
            timeout = input("Enter the custom timeout in seconds: ").strip()
            headers["X-Timeout"] = timeout
        elif choice == '11':
            wait_selector = input("Enter the CSS selector to wait for: ").strip()
            headers["X-Wait-For-Selector"] = wait_selector
        elif choice == '12':
            level_of_details = input("Enter the level of details: ").strip()
            headers["X-Level-Of-Details"] = level_of_details
    
    return headers

mode = input("Enter 'r' for reading a URL or 's' for searching a query: ").strip().lower()

if mode == 'r':
    url = input("Enter the URL to read: ").strip()
    full_url = f"https://r.jina.ai/{url}"
    headers = get_headers()
    response = requests.get(full_url, headers=headers)
    if headers.get("Accept") == "application/json":
        with open("response.json", "w", encoding="utf-8") as file:
            json.dump(response.json(), file, indent=4)
    else:
        with open("response.txt", "w", encoding="utf-8") as file:
            file.write(response.text)
elif mode == 's':
    query = input("Enter the search query: ").strip()
    full_url = f"https://s.jina.ai/{query}"
    headers = get_headers()
    response = requests.get(full_url, headers=headers)
    with open("response.json", "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4)
else:
    print("Invalid input. Please enter 'r' or 's'.")