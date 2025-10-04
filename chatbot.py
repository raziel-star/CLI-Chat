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
            bot_response = f"File '{file_path}' created successfully.\nCLI-Agent Feedback: {feedback}"

        elif "send email" in user_lower:
            try:
                parts = user_input.split(maxsplit=3)
                to_email, subject, body = parts[1], parts[2], parts[3]
                bot_response = send_email(to_email, subject, body, 'smtp.gmail.com', 465, 'YOUR_EMAIL', 'YOUR_PASSWORD')
            except:
                bot_response = "Invalid email command format."

        elif "search web" in user_lower:
            query = user_input[len("search web "):]
            bot_response = search_web(query)

        elif "run command" in user_lower:
            command = user_input[len("run command "):]
            bot_response = execute_system_command(command)

        else:
            bot_response = ai_response(user_input)

    except Exception as e:
        bot_response = f"Error during autonomous task execution: {e}"

    flag[0] = False
    t.join()

    return reverse_hebrew_advanced(bot_response)

def ai_response(user_input):
    prompt = (
        "You are CLI-Chat, a professional AI assistant created by raziel-star (GitHub user), "
        "based on a large language model trained by Google.\n\n"
        "Your tasks and abilities:\n"
        "- Respond in the same language as the user.\n"
        "- Answer general questions clearly and concisely.\n"
        "- Assist in learning, teaching, and research across multiple disciplines, including:\n"
        "    - Mathematics (basic to advanced)\n"
        "    - Languages (English grammar, vocabulary, translations)\n"
        "    - Science (Physics, Chemistry, Biology)\n"
        "    - History, Sociology, Philosophy, Psychology\n"
        "    - Economics, Finance, and Business concepts\n"
        "    - Technology, Computing, AI, and Cybersecurity\n"
        "    - Health and basic medical knowledge\n"
        "- Generate, review, or explain content in text, code, or structured data.\n"
        "- Create professional documents, summaries, and reports.\n"
        "- Provide feedback and improvement suggestions for user work or files.\n"
        "- Help with problem-solving, reasoning, logical explanations, and critical thinking.\n"
        "- Offer creative ideas, project planning, and guidance for learning or professional tasks.\n"
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

