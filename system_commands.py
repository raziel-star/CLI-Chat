import os

def execute_system_command(command):
    try:
        output = os.popen(command).read()
        return output or "Command executed successfully, no output."
    except Exception as e:
        return f"Failed to execute command: {e}"
