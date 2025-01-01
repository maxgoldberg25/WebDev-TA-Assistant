import os
import subprocess
import webbrowser
import time
import openai


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
    
    print("README file loaded. Parsing instructions...")
    
    for line in readme_content:
        line = line.strip()
        if not line or line.startswith("#"):  # Skip empty lines and comments
            continue
        
        print(f"Processing step: {line}")
        
        # If the line is a shell command
        if line.startswith("python") or line.startswith("pip") or line.startswith("cd"):
            try:
                subprocess.run(line, shell=True, check=True)
                print(f"Successfully executed: {line}")
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {line}\n{e}")
        
        # If the line requires explanation or is unclear
        else:
            print(f"Unclear instruction: {line}")
            response = get_openai_guidance(line, openai_api_key)
            print(f"OpenAI's guidance: {response}")


def get_openai_guidance(instruction, api_key):
    """
    Gets guidance from OpenAI API for an unclear instruction.
    
    Args:
        instruction (str): The unclear instruction from the README file.
        api_key (str): OpenAI API key.
    
    Returns:
        str: Explanation or guidance from OpenAI.
    """
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            model="gpt-4o-mini",
            prompt=f"Explain or provide clarification for the following instruction:\n\n{instruction}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error communicating with OpenAI API: {e}"

def install_dependencies(requirements_file, venv_python):
    """Install dependencies using pip in the venv."""
    if os.path.exists(requirements_file):
        print(f"Installing dependencies from {requirements_file}...")
        subprocess.run([venv_python, "-m", "pip", "install", "-r", requirements_file])
    else:
        print("No requirements.txt found. Skipping dependency installation.")

def run_files_with_venv(directory, venv_python, port=3000):
    """Run Python files using the virtual environment."""
    python_files = [f for f in os.listdir(directory) if f.endswith('.py')]

    if not python_files:
        print("No Python files found in the specified directory.")
        return

    for python_file in python_files:
        file_path = os.path.join(directory, python_file)
        print(f"Running: {python_file}")

        try:
            # Start the Python file with the venv Python interpreter
            process = subprocess.Popen(
                [venv_python, file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            time.sleep(3)  # Wait for the server to start

            # Open the local link in the web browser
            local_url = f"http://localhost:{port}"
            webbrowser.open(local_url)
            print(f"Opened {local_url} for {python_file}")

            # Wait for user input to proceed
            input("Press Enter to stop the server and proceed to the next file...")
        
        finally:
            # Terminate the server process
            process.terminate()
            print(f"Stopped server for {python_file}")

    print("All files have been processed.")


def find_readme(project_dir):
    """Find README.txt or similar files in the project directory."""
    readme_files = [f for f in os.listdir(project_dir) if f.lower().startswith("readme")]
    for readme_file in readme_files:
        if readme_file.lower().endswith(('.txt', '.md')):
            return os.path.join(project_dir, readme_file)
    return None

# Main execution logic
if __name__ == "__main__":
    project_dir = input("Enter the path to the project directory: ").strip()
    venv_dir = os.path.join(project_dir, "venv")
    requirements_path = os.path.join(project_dir, "requirements.txt")
    venv_python = os.path.join(venv_dir, "Scripts", "python") if os.name == "nt" else os.path.join(venv_dir, "bin", "python")

    if os.path.isdir(project_dir):
        try:
            setup_venv(venv_dir)
            install_dependencies(requirements_path, venv_python)

            readme_path = find_readme(project_dir)
            if readme_path:
                print(f"Found README file at: {readme_path}")
                openai_api_key = input("Enter your OpenAI API key: ").strip()
                execute_readme(readme_path, openai_api_key)
            else:
                print("No README file found in the project directory.")

            run_files_with_venv(project_dir, venv_python)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("The specified path is not a valid directory.")
