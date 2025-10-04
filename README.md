# CLI-Chat: An Intelligent Command Line Assistant

## 🚀 Overview

CLI-Chat is a powerful, multi-functional command-line interface assistant built using **Python** and the **Google Gemini API**. It transforms your terminal into a smart agent capable of holding natural conversations, providing coding assistance, and executing real-world tasks autonomously.

The assistant is designed with a clean, modular architecture, making it easy to extend and maintain.

## ✨ Key Features

* **Gemini-Powered Intelligence:** Utilizes the high-performance `gemini-2.5-flash` for fast conversations and the advanced `gemini-2.5-pro` for complex tasks like file content generation and feedback.
* **Autonomous Task Execution:** The agent intelligently detects and performs four primary real-world actions:
    * `create file [filename] [description]`: Generates a file (e.g., Python script, config file) with AI-written content based on the description.
    * `search web [query]`: Performs a real-time web search using SerpApi to provide current information and snippets.
    * `run command [system_command]`: Executes operating system commands (e.g., `ls`, `dir`, `git status`) directly.
    * `send email [to] [subject] [body]`: Handles basic email sending (requires setup).
* **Persistent Conversation Memory:** Utilizes `pickle` to save and load conversation history, ensuring context is maintained between sessions.
* **Modular Design:** Code is neatly separated into dedicated modules (e.g., `system_commands.py`, `file_handler.py`, `web_search.py`) for clarity and maintainability.
* **Interactive UX:** Features colorized output (`colorama`), a main menu for new/previous sessions, and a visual processing spinner with threading for a smooth user experience.
* **Multilingual Support:** Includes a specialized utility for correctly handling and reversing Hebrew text in the terminal.

## 🛠️ Setup and Installation

### Prerequisites

1.  Python 3.8+
2.  API Keys for Google Gemini and SerpApi.

### 1. Clone the Repository

```bash
git clone [YOUR_REPO_URL]
cd cli-chat
