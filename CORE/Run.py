import subprocess
import sys
import os

def run_python_file(file_path):
    try:
        # Ensure the working directory is set to the directory containing manage.py
        project_dir = os.path.dirname(os.path.abspath(file_path))
        
        # Commands to run before starting the server
        commands = [
            #[sys.executable, file_path, 'makemigrations'],
            #[sys.executable, file_path, 'migrate'],
            [sys.executable, file_path, 'runserver']
        ]
        
        for command in commands:
            process = subprocess.Popen(
                command,
                cwd=project_dir
            )
            process.wait()
            # Check if the command was successful
            if process.returncode != 0:
                print(f"Command {' '.join(command)} failed with return code {process.returncode}")
                return  # Exit if a command fails

    except Exception as e:
        print("An exception occurred:\n", str(e))

if __name__ == "__main__":
    file_to_run = 'manage.py'  # Path to your manage.py file
    run_python_file(file_to_run)
