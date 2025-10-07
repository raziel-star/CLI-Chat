# קובץ: main.py

from colorama import Fore, Style, init
from utils import clear_screen, typewriter, load_memory, save_memory
from chatbot import ai_response, handle_task, conversation_memory

init(autoreset=True)

def chat_loop():
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "🤖 CLI-Chat Active! Type 'exit' to quit.\n")

    task_keywords = ["create file", "send email", "search web", "run command"]

    while True:
        user_input = input(Fore.GREEN + "You: " + Style.RESET_ALL).strip()
        if user_input.lower() in ["exit", "quit"]:
            save_memory(conversation_memory)
            print(Fore.CYAN + "👋 Goodbye!")
            break

        user_input_lower = user_input.lower()
        conversation_memory.append(f"User: {user_input}")

        # לוגיקה מתוקנת: בודקים אם הקלט *מתחיל* באחת ממילות המפתח
        is_task = False
        for keyword in task_keywords:
            # בודקים אם הקלט מתחיל במילה המדויקת + רווח, או רק במילה המדויקת
            if user_input_lower.startswith(keyword + " ") or user_input_lower == keyword:
                result = handle_task(user_input)
                is_task = True
                break
        
        if not is_task:
            result = ai_response(user_input)

        conversation_memory.append(f"CLI-Chat: {result}")
        print(Fore.MAGENTA + "CLI-Chat: " + Style.RESET_ALL, end="")
        typewriter(result, delay=0.001)


def main_menu():
    global conversation_memory
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "🤖 Welcome to CLI-Chat type 'exit' to quit.\n")
    while True:
        print(Fore.YELLOW + "1. Start New Chat/Agent Session")
        print(Fore.YELLOW + "2. Continue Previous Session")
        print(Fore.YELLOW + "3. Exit\n")
        choice = input(Fore.GREEN + "Select an option (1/2/3): " + Style.RESET_ALL).strip()

        if choice == "1":
            conversation_memory = []
            chat_loop()
            break
        elif choice == "2":
            conversation_memory = load_memory()
            if conversation_memory:
                print(Fore.CYAN + "Loaded previous conversation.\n")
            else:
                print(Fore.RED + "No previous conversation found. Starting new session.\n")
                conversation_memory = []
            chat_loop()
            break
        elif choice == "3":
            print(Fore.CYAN + "👋 Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
