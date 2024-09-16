import os
import requests
import zipfile
import shutil
import tempfile
import colorama
from colorama import Fore, Style
import pyfiglet
from termcolor import colored

# Initialize colorama
colorama.init(autoreset=True)

# Constants
VERSION_URL = "https://vajeservices.xyz/stats/version"
DOWNLOAD_URL = "https://vajeservices.xyz/downloadvaje"
DESTINATION_DIR = os.path.expandvars(r"%appdata%\.minecraft\config\chattriggers\modules")

# Set the console title
os.system("cls")
os.system("title Vaje Installer (Made By Donskyblock)")

def print_rainbow_text(text):
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    ascii_art = pyfiglet.figlet_format(text)
    for i, line in enumerate(ascii_art.splitlines()):
        print(colored(line, colors[i % len(colors)]))

def get_version():
    response = requests.get(VERSION_URL)
    if response.status_code == 200:
        version_data = response.json()
        return version_data.get("Version")
    else:
        print(f"{Fore.RED}Failed to get version info. Status code: {response.status_code}")
        return None

def download_and_extract_vaje():
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "vaje.zip")
        
        # Download the zip file
        with requests.get(DOWNLOAD_URL, stream=True) as r:
            if r.status_code == 200:
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            else:
                print(f"{Fore.RED}Failed to download Vaje. Status code: {r.status_code}")
                return False
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the folder containing index.js
        for root, dirs, files in os.walk(temp_dir):
            if 'index.js' in files:
                return root

    return None

def copy_to_minecraft_folder(source_folder):
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    
    folder_name = os.path.basename(source_folder)
    destination_path = os.path.join(DESTINATION_DIR, folder_name)
    
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)  # Remove existing folder
    
    shutil.copytree(source_folder, destination_path)
    print(f"{Fore.GREEN}Copied {folder_name} to Minecraft's ChatTriggers modules directory.")

def main():
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
        extracted_folder = download_and_extract_vaje()
        if extracted_folder:
            # Copy the folder to Minecraft's config folder
            copy_to_minecraft_folder(extracted_folder)
        else:
            print(f"{Fore.RED}Failed to find the folder with index.js in the extracted content.")
    else:
        print(f"{Fore.YELLOW}Download cancelled.")

if __name__ == "__main__":
    main()
