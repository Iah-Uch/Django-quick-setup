"""
This script is designed to automate the setup and management of a Django project. It performs the following tasks:

1. Creates or recreates a virtual environment for the project.
2. Activates the virtual environment.
3. Installs project dependencies specified in the 'requirements.txt' file within the virtual environment.
4. Runs initial Django management commands (makemigrations, migrate, collectstatic).
5. Provides the option to start the Django development server, allowing it to be exposed to the network if desired.

Usage:
    python setup_and_run_django.py <requirements> <project_dir>

Arguments:
    <requirements>: Path to the requirements.txt file containing project dependencies.
    <project_dir>: Path to the project directory.

Notes:
- If a virtual environment already exists, the script prompts whether to reinstall the project or run management commands only.
- Proper security measures should be taken if exposing the server to the network.

Author: Iah-Uch
Contact: https://github.com/Iah-Uch/
Source: https://github.com/Iah-Uch/Django-quick-setup/
"""


import os
import argparse
import subprocess
import socket
import sys

# Function to run a shell command and handle errors
def run_command(command, **kwargs):
    section_name = kwargs.get("section_name")
    if section_name: 
        print(f"\033[94mRunning {section_name}...\033[0m")
    try:
        subprocess.run(command, shell=True, check=True)
        print("\n\033[92m\u2713  Done!\033[0m\n")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError: {e}\033[0m")
        sys.exit(1)

# Function to get the local IP address
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        s.connect(("8.8.8.8", 80))  # Connect to a public DNS server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")
        return None

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Function to create or recreate the virtual environment
def create_virtual_environment(venv_path):
    print("\033[97mCreating a virtual environment...\033[0m")
    run_command(f"python -m venv {venv_path}")

# Function to activate the virtual environment
def activate_virtual_environment(venv_path):
    activate_script = os.path.join(venv_path, "Scripts", "activate")
    run_command(activate_script)

# Function to install dependencies
def install_dependencies(venv_path, requirements_path):
    print("\033[97mInstalling project dependencies...\033[0m\n")
    run_command(f"{venv_path}\\Scripts\\pip install -r {requirements_path}")

# Function to run initial management commands
def run_initial_management_commands(venv_path, project_dir):
    print("\033[97mRunning initial management commands...\033[0m\n")
    run_command(f"{venv_path}\\Scripts\\python {os.path.join(project_dir, 'manage.py')} makemigrations", section_name="makemigrations")
    run_command(f"{venv_path}\\Scripts\\python {os.path.join(project_dir, 'manage.py')} migrate", section_name="migrate")
    run_command(f"{venv_path}\\Scripts\\python {os.path.join(project_dir, 'manage.py')} collectstatic --noinput", section_name="collectstatic")

# Function to start the Django development server
def start_django_server(venv_path, project_dir):
    start_server = input("\n\033[94mStart the Django development server? (y/n): \033[0m")
    if start_server.lower() == "y":
        expose_to_network = input("\n\033[93mExpose the server to the network? (y/n): \033[0m")
        if expose_to_network.lower() == "y":
            print("\n\033[91mWARNING: Exposing the server to the network may pose security risks.")
            print("Please ensure proper security measures are in place.")
            local_ip = get_local_ip()
            if local_ip:
                print(f"\n\033[92mYou can access the server from other devices on the network using this IP: {local_ip}:8000\033[0m")
            else:
                print("\n\033[91mUnable to determine the local IP address. You can manually find it and use it to access the server.\033[0m")
            run_command(f"{venv_path}\\Scripts\\python {os.path.join(project_dir, 'manage.py')} runserver 0.0.0.0:80", section_name="Django server")
        else:
            run_command(f"{venv_path}\\Scripts\\python {os.path.join(project_dir, 'manage.py')} runserver", section_name="Django server")

def main():
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description="Setup and run a Django project.")
        parser.add_argument("requirements", help="Path to the requirements.txt file (a virtual environment will be created in the directory of this script)")
        parser.add_argument("project_dir", help="Path to the project directory")
        args = parser.parse_args()

        # Determine the parent directory (where the virtual environment will be created)
        parent_dir = script_dir

        # Check if the virtual environment already exists
        venv_path = os.path.join(parent_dir, "venv")
        if os.path.exists(venv_path):
            reinstall_project = input("\033[93mA virtual environment already exists. Reinstall the project? (y/n): \033[0m")
            if reinstall_project.lower() == "n":
                run_management_commands = input("\033[93mRun the management commands anyway? (y/n): \033[0m")
                if run_management_commands.lower() == "y":
                    run_initial_management_commands(venv_path, args.project_dir)
                    start_django_server(venv_path, args.project_dir)
                print("\033[92mSetup completed without reinstalling the project.\033[0m")
                sys.exit(0)

        # Create or recreate the virtual environment
        create_virtual_environment(venv_path)

        # Activate the virtual environment
        activate_virtual_environment(venv_path)

        # Install project dependencies within the virtual environment
        install_dependencies(venv_path, args.requirements)

        # Run initial management commands within the virtual environment
        run_initial_management_commands(venv_path, args.project_dir)

        # Start the Django development server within the virtual environment
        start_django_server(venv_path, args.project_dir)

        print("\n\033[92mSetup and server run completed successfully!\033[0m")
        
    except KeyboardInterrupt:
        print("\n\033[91mKeyboardInterrupt. Exiting...\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()
