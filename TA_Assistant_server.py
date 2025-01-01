import os
import subprocess
import webbrowser
import time
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#* Access keys from the .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def setup_venv(venv_path): 
    """Create and activate a virtual environment if not already existing."""
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        subprocess.run(["python3", "-m", "venv", venv_path])
        print(f"Virtual environment created at {venv_path}")

    print("Activating virtual environment...")
    activate_script = os.path.join(venv_path, "Scripts", "activate") if os.name == "nt" else os.path.join(venv_path, "bin", "activate")
    if not os.path.exists(activate_script):
        raise FileNotFoundError("Activation script not found. Check the venv setup.")
    return activate_script

def execute_readme(readme_path, openai_api_key): 
    """
    Executes steps from a README.txt file and provides assistance via OpenAI API.
    
    Args:
        readme_path (str): Path to the README.txt file.
        openai_api_key (str): OpenAI API key for guidance on steps.
    """
    # Check if the README file exists
    if not os.path.isfile(readme_path):
        print(f"README file not found at: {readme_path}")
        return
    
    # Read the README file
    with open(readme_path, 'r') as file:
        readme_content = file.readlines()
    
    print("README file loaded. Sending full content to OpenAI API for guidance...")

    response = get_openai_guidance(readme_content, openai_api_key)
    print("OpenAI's guidance on the README:\n")
    print(response)


def get_openai_guidance(instruction, api_key):
    """
    Gets guidance from OpenAI API for an unclear instruction.
    
    Args:
        instruction (str): The unclear instruction from the README file.
        api_key (str): OpenAI API key.
    
    Returns:
        str: Explanation or guidance from OpenAI.
    """
    client = openai.OpenAI(
    api_key=api_key,
    )

    prompt=(f"Explain or provide clarification for the following instruction:\n\n{instruction}")

    try:
        completion = client.chat.completions.create(
        model="gpt-4o-mini",  # GPT-4 Turbo model
        messages=[
            {"role": "system", "content": "You are a TA for a webdev class. Students include instructions on how to run the code in the readme, sometimes they are not clear so you are in charge of determining what is meant in the readme. All you need to output is the exact command line instructions to run the code. An example would be 'python3 app.py'"},
            {"role": "user", "content": prompt}
        ],    
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error communicating with OpenAI API: {e}"

def install_dependencies(requirements_file, venv_python): 
    """Install dependencies using pip in the venv."""
    # Check for both uppercase and lowercase variations
    if not os.path.exists(requirements_file):
        alt_requirements_file = requirements_file.replace("requirements.txt", "Requirements.txt")
        if os.path.exists("Requirements.txt"):
            requirements_file = alt_requirements_file
        else:
            print("No requirements.txt or Requirements.txt found. Skipping dependency installation.")
            return

    print(f"Installing dependencies from {requirements_file}...")
    subprocess.run([venv_python, "-m", "pip", "install", "-r", requirements_file])


def run_files_with_venv(project_dir, venv_python):
    """Run Flask files in the project directory."""
    flask_files = [f for f in os.listdir(project_dir) if os.path.isdir(os.path.join(project_dir, f)) or f.endswith(".py")]

    for flask_file in flask_files:
        if (flask_file != "run.py"):
            print(f"Skipping file: {flask_file}")
            continue # Skip files that are not app.py
        file_path = os.path.join(project_dir, flask_file)

        if os.path.isdir(file_path):
            print(f"Running Flask app from folder: {flask_file}")
            command = [venv_python, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
        else:
            print(f"Running Flask app: {flask_file}")
            command = [venv_python, file_path]

        try:
            env = os.environ.copy()
            env["FLASK_APP"] = file_path if not os.path.isdir(file_path) else flask_file
            env["FLASK_ENV"] = "development"
            env["FLASK_RUN_HOST"] = "0.0.0.0"
            env["FLASK_RUN_PORT"] = "5000"

            process = subprocess.Popen(command, cwd=project_dir, env=env)
            print(f"Started Flask app: {flask_file} on http://127.0.0.1:5000")

            # Open the correct link in the browser
            webbrowser.open("http://127.0.0.1:5000")

            input("Press Enter to stop the app and proceed to the next...")
            process.terminate()
        except Exception as e:
            print(f"Error running Flask app {flask_file}: {e}")


def find_readme(project_dir):
    """Find README.txt or similar files in the project directory."""
    readme_files = [f for f in os.listdir(project_dir) if f.lower().startswith("readme")]
    for readme_file in readme_files:
        if readme_file.lower().endswith(('.txt', '.md')):
            return os.path.join(project_dir, readme_file)
    return None

if __name__ == "__main__":
    project_dir = input("Enter the path to the project directory: ").strip() 
    venv_dir = os.path.join(project_dir, "venv") # Virtual environment directory
    requirements_path = os.path.join(project_dir, "Requirements.txt") # Requirements file path
    print(f"Project directory: {project_dir}") # Print the project directory
    venv_python = os.path.join(venv_dir, "Scripts", "python") if os.name == "nt" else os.path.join(venv_dir, "bin", "python") # Virtual environment Python path

    if os.path.isdir(project_dir): # Check if the project directory exists
        try:
            setup_venv(venv_dir)
            install_dependencies(requirements_path, venv_python)

            readme_path = find_readme(project_dir)
            if readme_path:
                print(f"Found README file at: {readme_path}")
                openai_api_key = OPENAI_API_KEY
                #execute_readme(readme_path, openai_api_key)
            else:
                print("No README file found in the project directory.")

            run_files_with_venv(project_dir, venv_python)
        except Exception as e:
            print(f"Error: {e}")
    else: # If the specified path is not a valid directory
        print("The specified path is not a valid directory.")

