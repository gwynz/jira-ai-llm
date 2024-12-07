# Import necessary libraries
import requests
import json
import asyncio
from openai import AsyncOpenAI
from termcolor import colored
import os

# Get the OpenAI API key from environment variables or use a placeholder
openai_api_key = os.getenv("OPENAI_API_KEY") or "enter your openai api key here"

# Flag to show options
SHOW_OPTIONS = False

# Initialize the OpenAI client with the API key
openai = AsyncOpenAI(api_key=openai_api_key)

# Function to call GPT-4 with streaming and JSON response
async def call_gpt4_with_streaming(messages):
    # Make an asynchronous request to the OpenAI API
    response = await openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True
    )
    assistant_response = ""
    # Process the streaming response
    async for chunk in response:
        if chunk.choices[0].delta.content is not None:
            assistant_response += chunk.choices[0].delta.content
            print(colored(chunk.choices[0].delta.content, 'green'), end="", flush=True)
    return assistant_response

# Function to get headers based on user input
def get_headers(SHOW_OPTIONS=True):
    if not SHOW_OPTIONS:
        return {}
    headers = {}
    # Prompt user for Jina API key
    api_key = input(colored("Enter your Jina API key (or leave blank to skip): ", 'cyan')).strip()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    # List of options for the user to choose from
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
    
    # Prompt user to choose options
    print(colored("Choose options by entering their numbers, separated by commas:", 'cyan'))
    for option in options:
        print(colored(option, 'yellow'))
    
    # Process user choices
    choices = input(colored("Enter your choices: ", 'cyan')).strip().split(',')
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
            cookie = input(colored("Enter your cookie settings: ", 'cyan')).strip()
            headers["X-Set-Cookie"] = cookie
        elif choice == '6':
            proxy = input(colored("Enter your proxy URL: ", 'cyan')).strip()
            headers["X-Proxy-Url"] = proxy
        elif choice == '7':
            headers["X-No-Cache"] = "true"
        elif choice == '8':
            headers["Accept"] = "text/event-stream"
        elif choice == '9':
            selector = input(colored("Enter the CSS selector: ", 'cyan')).strip()
            headers["X-Target-Selector"] = selector
        elif choice == '10':
            timeout = input(colored("Enter the custom timeout in seconds: ", 'cyan')).strip()
            headers["X-Timeout"] = timeout
        elif choice == '11':
            wait_selector = input(colored("Enter the CSS selector to wait for: ", 'cyan')).strip()
            headers["X-Wait-For-Selector"] = wait_selector
        elif choice == '12':
            level_of_details = input(colored("Enter the level of details: ", 'cyan')).strip()
            headers["X-Level-Of-Details"] = level_of_details
    
    return headers

# Function to handle 'read URL' mode
async def handle_mode_r(messages):
    # Prompt user for URL
    url = input(colored("Enter the URL to read: ", 'cyan')).strip()
    full_url = f"https://r.jina.ai/{url}"
    headers = get_headers(SHOW_OPTIONS)
    # Make a GET request to the URL
    response = requests.get(full_url, headers=headers)
    content = response.text
    # Save the response content to a file
    with open("response.txt", "w", encoding="utf-8") as file:
        file.write(content)
    # Update messages based on user input
    if not messages:
        messages = [{"role": "system", "content": f"please answer user questions based on all the contents provided: \n\n initial content:\n {content}"}]
    else:
        action = input(colored("Do you want to add this content to the context or replace it? (a/r): ", 'cyan')).strip().lower()
        if action == 'a':
            for message in messages:
                if message["role"] == "system":
                    message["content"] += f"\n\n additional content: \n{content}"
                    break
        elif action == 'r':
            messages = [{"role": "system", "content": f"please answer user questions based on all the contents provided: \n\n initial content:\n {content}"}]
        else:
            print(colored("Invalid input. Content not added.", 'red'))
    return messages

# Function to handle 'search query' mode
async def handle_mode_s(messages):
    # Prompt user for search query
    query = input(colored("Enter the search query: ", 'cyan')).strip()
    full_url = f"https://s.jina.ai/{query}"
    headers = {"Accept": "application/json"}
    # Make a GET request to the search URL
    response = requests.get(full_url, headers=headers)
    response_json = response.json()
    content = json.dumps(response_json, indent=4)
    # Save the response JSON to a file
    with open("response.json", "w", encoding="utf-8") as file:
        json.dump(response_json, file, indent=4)

    # Update messages based on user input
    if not messages:
        messages = [{"role": "system", "content": f"please answer user questions based on all the contents provided: \n\n initial content:\n {content}"}]
    else:
        while True:
            action = input(colored("Do you want to add this content to the context or replace it? (a/r): ", 'cyan')).strip().lower()
            if action in ['a', 'r']:
                break
            else:
                print(colored("Invalid input. Please enter 'a' to add or 'r' to replace.", 'red'))
        if action == 'a':
            for message in messages:
                if message["role"] == "system":
                    message["content"] += f"\n\n additional content: \n{content}"
                    break
        elif action == 'r':
            messages = [{"role": "system", "content": f"please answer user questions based on all the contents provided: \n\n initial content:\n {content}"}]
        else:
            print(colored("Invalid input. Content not added.", 'red'))
    return messages

# Function to handle 'new conversation' mode
async def handle_mode_n(messages):
    messages = []
    print(colored("Started a new conversation.", 'green'))
    return messages

# Main chat loop function
async def chat_loop(messages):
    while True:
        # Prompt user for input
        user_input = input(colored("\nYou: ", 'cyan')).strip()
        if user_input.lower() in ['exit', 'quit']:
            break
        elif user_input.lower() == 'new':
            messages = await handle_mode_n(messages)
            await main_loop(messages)
            continue  # Continue to allow adding to the conversation
        elif user_input.lower() == 'add':
            await main_loop(messages)  # Go back to main loop to add more content
            continue
        messages.append({"role": "user", "content": user_input})
        # Call GPT-4 and get the assistant's response
        assistant_response = await call_gpt4_with_streaming(messages)
        messages.append({"role": "assistant", "content": assistant_response})

# Main loop function to handle different modes
async def main_loop(messages):
    while True:
        # Prompt user to choose a mode
        mode = input(colored("Enter 'r' for reading a URL, 's' for searching a query, 'n' to start a new conversation, or press Enter to continue chatting: ", 'cyan')).strip().lower()
        if mode == 'r':
            messages = await handle_mode_r(messages)
        elif mode == 's':
            messages = await handle_mode_s(messages)
        elif mode == 'n':
            messages = await handle_mode_n(messages)
        else:
            await chat_loop(messages)

# Main function to start the program
async def main():
    messages = []
    await main_loop(messages)

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())
