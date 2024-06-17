# 🔍 Code Opus Interpreter

Welcome to **Code Opus Interpreter**! This innovative Python data science platform enables you to leverage **Anthropic's Claude** alongside a **secure sandbox** to dynamically generate and execute Python code. With the combination of Claude and the **Code Interpreter API by e2b**, we provide a seamless, interactive environment that streamlines your coding workflow.

The script and this README were entirely crafted by **claude-opus**.

## Key Features

### 1. **Claude as Your AI Data Expert**

- **Integration with Anthropic Claude API**: Utilize Claude-3 as your AI-driven data scientist.
- **On-the-Fly Code Generation**: Produce Python code tailored to your inputs.
- **Seamless Execution**:
 - Run Python code securely.
 - Retrieve results, logs, and visualizations.

### 2. **Advanced Code Interpreter API**

- **Execute Python Code**: Operate Python code in a Jupyter notebook-like environment.
- **Management of Files and Logs**: Store results, error tracebacks, and logs for future reference.
- **Integrated Tools**:
 - **execute_python**: Run Python code within an isolated cell.

### 3. **Secure and Controlled Execution**

- **Protected Python Sandbox**: Execute Python code in a secure and controlled environment.
- **Access to Filesystem**:
 - Perform read/write operations.
 - Download files generated during execution.

## Getting Started

### Prerequisites

1. **Python**: Ensure Python 3.8 or higher is installed.
2. **API Keys**:
  - **Anthropic Claude API Key**.
  - **E2B Code Interpreter API Key**.

### Installation Steps

1. **Clone the Repository**:
  ```bash
  git clone https://github.com/sormind/CodeOpus.git
  cd CodeOpus
  `2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt`

1.  **Create a `.env` File**: Add your API keys to a `.env` file in the root directory:

    ini

    Copy

    `# .env file
    ANTHROPIC_API_KEY=<your_anthropic_api_key>
    E2B_API_KEY=<your_e2b_api_key>`

### Usage

1.  **Run the Script**:

    bash

    Copy

    `python code_opus.py`

2.  **Interact with Claude**:
    -   Input your queries to request code snippets or data analysis.
    -   Use `quit` to exit the program.

Example Queries
---------------

-   **Data Analysis**: "Provide a summary of this dataset."
-   **Visualization**: "Generate a scatter plot comparing variables X and Y."
-   **Code Generation**: "Create a Python function to compute Fibonacci numbers."

Inner Workings
--------------

### How It Functions

1.  **System Prompt**: Configures Claude as a Python data scientist.
2.  **Tool Definition**:
    -   `execute_python`: Runs Python code in a secure environment.
3.  **Chat Functionality**:
    -   **chat**: Processes user inputs and interprets Claude's responses.
    -   **code_interpret**: Executes Python code and handles results, logs, and files.

Contributing
------------

All data enthusiasts and coding wizards are invited to contribute! You can:

-   Create issues for bug reports or feature requests.
-   Submit pull requests with enhancements.

License
-------

This project is licensed under the MIT License.

Don't hesitate to reach out with inquiries or ideas. Remember, **Claude** and the **Code Interpreter** are here to elevate your data science journey!