import threading
from colorama import Fore
from google import genai
from utils import dots_spinner, reverse_hebrew_advanced, extract_text
from file_handler import create_file, generate_feedback
from email_sender import send_email
from web_search import search_web
from system_commands import execute_system_command
import config

client = genai.Client(api_key=config.GOOGLE_API_KEY)
conversation_memory = []

def handle_task(user_input):
    conversation_memory.append(f"CLI-Agent: Planning task for input '{user_input}'...")

    flag = [True]
    t = threading.Thread(target=dots_spinner, args=(flag, "CLI-Agent planning task", Fore.YELLOW))
    t.start()

    bot_response = ""
    try:
        user_lower = user_input.lower()
        
        if "create file" in user_lower:
            parts = user_input.split(maxsplit=2)
            filename = parts[2].split()[0]
            description = " ".join(parts[2].split()[1:]) or "Fill file content based on AI reasoning."
            file_prompt = f"Create a file named '{filename}' with content based on: {description}"
            resp = client.models.generate_content(model="gemini-2.5-pro", contents=[file_prompt])
            file_content = extract_text(resp)
            file_path = create_file(filename, file_content)

            feedback = generate_feedback(filename, file_content, client)
            bot_response = f"File '{file_path}' created successfully.\nCLI-Agent Feedback:\n{feedback}"

        elif "send email" in user_lower:
            try:
                command_tail = user_input[len("send email"):].strip()
                parts = command_tail.split("|", maxsplit=2) 
                
                if len(parts) == 3:
                    to_email = parts[0].strip()
                    subject = parts[1].strip()
                    body = parts[2].strip()
                    
                    bot_response = send_email(
                        to_email, subject, body, 
                        config.SMTP_SERVER, config.SMTP_PORT, 
                        config.SENDER_USERNAME, config.SENDER_PASSWORD
                    )
                else:
                    bot_response = "Invalid email command format. Use: send email <TO_EMAIL> | <SUBJECT> | <BODY>"

            except Exception as e:
                bot_response = f"Error during email processing: {e}"

        elif "search web" in user_lower:
            try:
                query = user_input[len("search web"):].strip()
                if not query:
                    bot_response = "Please provide a query for web search."
                else:
                    raw_results = search_web(query)
                    
                    if "No results found." in raw_results or "Search failed:" in raw_results:
                        bot_response = raw_results
                    else:
                        # שימוש ב-AI לסיכום וניסוח התוצאות
                        summary_prompt = (
                            f"You are CLI-Chat, a professional AI assistant. The user requested to search the web for: '{query}'. "
                            f"The raw results snippets are:\n---\n{raw_results}\n---\n"
                            "Based on the raw results, provide a professional, friendly, and concise summary that answers the user's query directly. Do not use markdown (e.g. bold, lists)."
                        )
                        summary_resp = client.models.generate_content(
                            model="gemini-2.5-flash", 
                            contents=[summary_prompt]
                        )
                        bot_response = extract_text(summary_resp)

            except Exception as e:
                bot_response = f"Error during web search: {e}"

        elif "run command" in user_lower:
            try:
                command = user_input[len("run command"):].strip()
                if not command:
                    bot_response = "Please provide a command to run."
                else:
                    raw_output = execute_system_command(command)
                    
                    analysis_prompt = (
                        f"You are CLI-Chat, a professional AI assistant. The user executed the system command: '{command}'. "
                        f"The raw command output is:\n---\n{raw_output}\n---\n"
                        "Analyze the output. Explain concisely what happened (e.g., 'The files in the current directory are...' or 'The command executed successfully, but returned an empty output.'). Your response must be in clear, natural language and highly relevant to the command output."
                    )
                    analysis_resp = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=[analysis_prompt]
                    )
                    bot_response = extract_text(analysis_resp)

            except Exception as e:
                bot_response = f"Error executing command: {e}"

        else:
            bot_response = "Task not recognized. Please use one of the predefined tasks (create file, send email, search web, run command)."

    except Exception as e:
        bot_response = f"An unexpected error occurred during task handling: {e}"

    flag[0] = False
    t.join()
    conversation_memory.append(f"CLI-Agent: Task handled, response is: {bot_response}")

    return reverse_hebrew_advanced(bot_response)

def ai_response(user_input):
    prompt = (
        "You are CLI-Chat, an advanced, professional AI assistant for the command-line, built using the Gemini API. "
        "Your primary functions include:\n"
        "- Providing expert assistance, planning, and guidance for learning or professional tasks.\n"
        "- Assist with exam preparation, exercises, and simulations.\n"
        "- Analyze information, identify patterns, and provide insights or summaries.\n"
        "- Suggest coding solutions, debug code, and provide explanations.\n"
        "- Provide professional advice on learning, productivity, and time management.\n"
        "- Initiate autonomous tasks when relevant.\n"
        "- Plan and prioritize tasks proactively, based on user needs or context.\n\n"
        "Conversation handling:\n"
        "- Use conversation memory to maintain context and continuity.\n"
        "-don't use markdown"
        "- Keep responses concise, clear, and professional.\n"
        "- Ask clarifying questions if user instructions are ambiguous.\n"
        "- Always provide structured, logical, and actionable guidance when possible.\n\n"
        "You can run cmd commands.\n"
        "Conversation so far:\n" + "\n".join(conversation_memory) + f"\nUser: {user_input}\nCLI-Agent:"
    )

    flag = [True]
    t = threading.Thread(target=dots_spinner, args=(flag, "CLI-Agent Thinking", Fore.BLUE))
    t.start()

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=[prompt])
        bot_response = extract_text(response)
    except Exception as e:
        bot_response = f"Error communicating with Gemini: {e}"

    flag[0] = False
    t.join()

    return reverse_hebrew_advanced(bot_response)
