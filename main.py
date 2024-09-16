import os
import sys
import requests
import zipfile
import shutil
import tempfile
import colorama
from colorama import Fore
import pyfiglet
from termcolor import colored

# Initialize colorama
colorama.init(autoreset=True)

# Determine the correct directory for bundled executables
if getattr(sys, 'frozen', False):
    # If the script is packaged using PyInstaller
    script_dir = sys._MEIPASS
else:
    # If the script is run normally
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Constants
VERSION_URL = "https://vajeservices.xyz/stats/version"
DOWNLOAD_URL = "https://vajeservices.xyz/downloadvaje"
DESTINATION_DIR = os.path.expandvars(r"%appdata%\.minecraft\config\chattriggers\modules")

# Clear the console
def clear_console():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Mac/Linux
        os.system('clear')

# Set the console title
def set_console_title(title):
    if os.name == 'nt':  # Windows
        os.system(f'title {title}')
    else:
        print(f"\033]0;{title}\a", end='', flush=True)

# Function to print rainbow ASCII art text
def print_rainbow_text(text):
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    ascii_art = pyfiglet.figlet_format(text)
    for i, line in enumerate(ascii_art.splitlines()):
        print(colored(line, colors[i % len(colors)]))

# Function to get the latest version from the API
def get_version():
    try:
        response = requests.get(VERSION_URL)
        if response.status_code == 200:
            version_data = response.json()
            return version_data.get("Version")
        else:
            print(f"{Fore.RED}Failed to get version info. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"{Fore.RED}Error fetching version info: {str(e)}")
        return None

# Function to download and extract Vaje
def download_and_extract_vaje(temp_dir):
    try:
        zip_path = os.path.join(temp_dir.name, "vaje.zip")
        
        # Download the zip file
        with requests.get(DOWNLOAD_URL, stream=True) as r:
            if r.status_code == 200:
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            else:
                print(f"{Fore.RED}Failed to download Vaje. Status code: {r.status_code}")
                return None
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir.name)
        
        # Print the contents of the extraction directory for debugging
        print(f"{Fore.YELLOW}Extracted files:")
        for root, dirs, files in os.walk(temp_dir.name):
            print(f"Root: {root}")
            for d in dirs:
                print(f"Dir: {d}")
            for f in files:
                print(f"File: {f}")

        # Find the folder containing index.js
        for root, dirs, files in os.walk(temp_dir.name):
            if 'index.js' in files:
                return root

        print(f"{Fore.RED}index.js file not found in the extracted content.")
        return None

    except Exception as e:
        print(f"{Fore.RED}Error during download or extraction: {str(e)}")
        return None

# Function to copy the folder to Minecraft's ChatTriggers directory
def copy_to_minecraft_folder(source_folder):
    try:
        if not os.path.exists(DESTINATION_DIR):
            os.makedirs(DESTINATION_DIR)
        
        folder_name = os.path.basename(source_folder)
        destination_path = os.path.join(DESTINATION_DIR, folder_name)

        # Debug information
        print(f"{Fore.YELLOW}Source Folder: {source_folder}")
        print(f"{Fore.YELLOW}Destination Path: {destination_path}")

        if not os.path.exists(source_folder):
            print(f"{Fore.RED}Source folder does not exist: {source_folder}")
            return
        
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)  # Remove existing folder
        
        shutil.copytree(source_folder, destination_path)
        print(f"{Fore.GREEN}Copied {folder_name} to Minecraft's ChatTriggers modules directory.")
    except Exception as e:
        print(f"{Fore.RED}Failed to copy to Minecraft folder: {str(e)}")

# Main function
def main():
    temp_dir = tempfile.TemporaryDirectory()
    try:
        # Clear console and set title
        clear_console()
        set_console_title("Vaje Installer (Made By Donskyblock)")
        
        # Print rainbow ASCII art banner
        print_rainbow_text("Vaje Installer")
        
        # Get the latest version
        version = get_version()
        if not version:
            print(f"{Fore.RED}Could not fetch the version. Exiting.")
            return
        
        # Prompt the user
        user_input = input(f"{Fore.GREEN}Are you sure you want to download Vaje {version}? Type Y to continue or N to close: ").strip().lower()
        
        if user_input == 'y':
            # Download and extract the zip file
            extracted_folder = download_and_extract_vaje(temp_dir)
            if extracted_folder:
                # Copy the folder to Minecraft's config folder
                copy_to_minecraft_folder(extracted_folder)
            else:
                print(f"{Fore.RED}Failed to find the folder with index.js in the extracted content.")
        else:
            print(f"{Fore.YELLOW}Download cancelled.")
    
    finally:
        # Cleanup the temporary directory
        temp_dir.cleanup()

if __name__ == "__main__":
    main()
