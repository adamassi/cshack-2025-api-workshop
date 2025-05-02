# Technion CS Hackathon 2025 AI&API Workshop

## Introduction
This repo holds the code for the AI&API workshop at the Technion CS Hackathon 2025.
In this workshop, we will learn how to use some examples of APIs that can help you in the hackathon.
In the technical part, we will learn how to build a simple Telegram bot that can summarize text from links using Firecrawl and OpenRouter APIs.

## Prerequisites
- Python installed on your machine (3.8 or higher, preferably 3.11)
- Basic knowledge of Python programming
- Telegram account and the Telegram app installed on your computer or phone
- An OpenRouter account (https://openrouter.ai/)
- A Firecrawl account (https://firecrawl.com/)

## Setup
1. Clone the repository:
   ```bash
    git clone
    cd hackathon-2025-ai-api-workshop
    ```
2. Create a virtual environment:
  ```bash
    conda create -n hackathon python=3.11
    conda activate hackathon
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. From here it's up to you how to handle your environment variables. In the `app.py` file we show several options for that.
   Several options are:
    - Use a `.env` file: 
      - Use the `python-dotenv` package to load environment variables from a `.env` file.
      - Create a `.env` file in the root directory of the project and add your API keys:
        ```bash
        OPENROUTER_API_KEY=your_openrouter_api_key
        FIRECRAWL_API_KEY=your_firecrawl_api_key
        TELEGRAM_BOT_TOKEN=your_telegram_bot_token
        ```
    - Use environment variables:
      Set the environment variables in your terminal:
      ```bash
      export OPENROUTER_API_KEY=your_openrouter_api_key
      export FIRECRAWL_API_KEY=your_firecrawl_api_key
      export TELEGRAM_BOT_TOKEN=your_telegram_bot_token
      ```
    - Use a config file:
      Create a `secrets.py` file in the root directory of the project and add your API keys:
      ```python
      OPENROUTER_API_KEY = 'your_openrouter_api_key'
      FIRECRAWL_API_KEY = 'your_firecrawl_api_key'
      TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
      ```
5. Run the bot:
    ```bash
    python app.py
    ```
6. Open Telegram and search for your bot using the username you set when creating the bot.
7. Start a chat with your bot. Use `/help` or `/start` commands to check if everything works. Then use the `/ask <LINK>` command to ask the bot to summarize a link.