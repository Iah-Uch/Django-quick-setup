# Django-quick-setup
This script is designed to automate the initial setup of a Django project. It performs the following tasks:

1. Creates a virtual environment for the project.
2. Activates the virtual environment.
3. Installs project dependencies specified in the 'requirements.txt' file within the virtual environment.
4. Runs initial Django management commands (makemigrations, migrate, collectstatic).
5. Provides the option to start the Django development server, allowing it to be exposed to the network if desired.

Usage:
    ```python quick_setup.py <requirements> <project_dir>```

Arguments:
   - ``<requirements>``: Path to the requirements.txt file containing project dependencies.
   - ``<project_dir>``: Path to the project directory.

Notes:
- If a virtual environment already exists, the script prompts whether to reinstall the project or run management commands only.
- Proper security measures should be taken if exposing the server to the network.
