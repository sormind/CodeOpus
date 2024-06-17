import os
import base64
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
from anthropic import Anthropic
from typing import List, Tuple
from e2b_code_interpreter import CodeInterpreter, Result
from e2b_code_interpreter.models import Logs
from e2b import Sandbox

# Load environment variables from .env file
load_dotenv()

# Initialize Anthropic client and sandbox
client = Anthropic()
sandbox = Sandbox(template="base")

# Configuration
MODEL_NAME = "claude-3-opus-20240229"

SYSTEM_PROMPT = """
## Your Role & Context
You are an AI-powered Python data scientist. Your tasks involve analyzing data, generating visualizations, and providing insights using Python code.
- The Python code runs in a Jupyter notebook environment.
- Each call to the `execute_python` tool runs the code in a separate cell. You can make multiple calls to `execute_python` as needed.
- Visualizations can be displayed using matplotlib or other libraries directly in the notebook.
- You have internet access and can make API requests.
- You have filesystem access for reading and writing files.
- You can install any required pip package (if available), but common data analysis packages are preinstalled.
- All code runs securely in a sandboxed environment.
"""

tools = [
    {
        "name": "execute_python",
        "description": "Execute Python code in a Jupyter notebook cell and return results, stdout, stderr, display data, and errors.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The Python code to execute in a single cell."
                }
            },
            "required": ["code"]
        }
    }
]

def execute_code(code_interpreter: CodeInterpreter, code: str):
    print(f"\n{'='*50}\n> Executing AI-generated code:\n{code}\n{'='*50}")
    execution = code_interpreter.notebook.exec_cell(code)

    if execution.error:
        error_message = f"Execution error: {execution.error.name}: {execution.error.value}.\n{execution.error.traceback}"
        print("[Code Interpreter Error]", error_message)
        return [], Logs(), error_message, []

    result_message = ""
    saved_files = []

    if execution.results:
        result_message = "Execution Results:\n"
        for i, result in enumerate(execution.results, start=1):
            result_message += f"Result {i}:\n"
            if result.is_main_result:
                result_message += f"[Main Result]: {result.text}\n"
            else:
                result_message += f"[Display Data]: {result.text}\n"

            # Check for file data and save files
            for file_type in ['png', 'jpeg', 'svg', 'pdf', 'html', 'json', 'javascript', 'markdown', 'latex']:
                file_data = getattr(result, file_type, None)
                if file_data:
                    file_extension = file_type
                    local_filename = f"output_file_{i}.{file_extension}"
                    sandbox_path = f"/home/user/{local_filename}"
                    
                    try:
                        # Write file inside sandbox
                        sandbox.filesystem.write_bytes(sandbox_path, base64.b64decode(file_data))

                        # Download file
                        file_in_bytes = sandbox.download_file(sandbox_path)
                        with open(local_filename, "wb") as file:
                            file.write(file_in_bytes)
                        saved_files.append(local_filename)
                        print(f"Saved: {local_filename}")
                    except Exception as e:
                        print(f"Failed to download {sandbox_path}: {str(e)}")
                    break

        print(result_message)

    if execution.logs.stdout or execution.logs.stderr:
        log_message = "Logs:\n"
        if execution.logs.stdout:
            log_message += f"Stdout: {' '.join(execution.logs.stdout)}\n"
        if execution.logs.stderr:
            log_message += f"Stderr: {' '.join(execution.logs.stderr)}\n"
        result_message += log_message
        print(log_message)

    if not result_message:
        result_message = "No output from execution."
        print(result_message)

    return execution.results, execution.logs, result_message, saved_files

def process_message(code_interpreter: CodeInterpreter, user_message: str) -> Tuple[List[Result], Logs, str, List[str]]:
    print(f"\n{'='*50}\nUser Message: {user_message}\n{'='*50}")

    message = client.beta.tools.messages.create(
        model=MODEL_NAME,
        system=SYSTEM_PROMPT,
        max_tokens=4096,
        messages=[{"role": "user", "content": user_message}],
        tools=tools,
    )

    print(f"\n{'='*50}\nModel Response: {message.content}\n{'='*50}")

    if message.stop_reason == "tool_use":
        tool_use = next(block for block in message.content if block.type == "tool_use")
        tool_name = tool_use.name
        tool_input = tool_use.input

        print(f"\n{'='*50}\nUsing Tool: {tool_name}\n{'='*50}")

        if tool_name == "execute_python":
            return execute_code(code_interpreter, tool_input["code"])
    return [], Logs(), "No code execution requested.", []

def main():
    try:
        while True:
            user_message = input("Enter your message (or 'quit' to exit): ")
            if user_message.lower() == 'quit':
                break

            with CodeInterpreter() as code_interpreter:
                try:
                    results, logs, result_message, saved_files = process_message(
                        code_interpreter,
                        user_message,
                    )
                except ValueError as e:
                    print(f"Error processing results: {e}")
                    continue

                print(logs)
                print(result_message)

                if saved_files:
                    print("Saved Files:")
                    for file in saved_files:
                        print(f"- {file}")
    finally:
        sandbox.close()

if __name__ == "__main__":
    main()