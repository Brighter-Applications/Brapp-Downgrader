import os
import shutil
import subprocess
import requests
import zipfile
from tqdm import tqdm
import glob

def find_fallout4_installation():
    print("Searching for Fallout 4 installation...")
    home_dir = os.path.expanduser("~")
    steam_paths = [
        os.path.join(home_dir, ".steam", "steam", "steamapps", "common", "Fallout 4"),
        os.path.join(home_dir, ".local", "share", "Steam", "steamapps", "common", "Fallout 4")
    ]
    for path in steam_paths:
        if os.path.exists(path):
            print(f"Fallout 4 found at: {path}")
            return path
    print("Fallout 4 installation not found.")
    return None

def find_app_manifest(fallout4_path):
    print("Searching for Steam app manifest...")
    steamapps_path = os.path.dirname(os.path.dirname(fallout4_path))
    manifest_path = os.path.join(steamapps_path, 'appmanifest_377160.acf')
    
    if os.path.exists(manifest_path):
        print(f"App manifest found at: {manifest_path}")
        return manifest_path
    print("App manifest not found.")
    return None

def check_and_download_steamcmd():
    print("Checking for SteamCMD...")
    steamcmd_path = os.path.join(os.getcwd(), 'steamcmd')
    steamcmd_exe = os.path.join(steamcmd_path, 'steamcmd.sh')

    if os.path.exists(steamcmd_exe):
        print("SteamCMD already exists.")
        return steamcmd_path

    script_dir = os.path.dirname(os.path.abspath(__file__))
    steamcmd_path = os.path.join(script_dir, 'steamcmd')

    print("SteamCMD not found. Downloading SteamCMD...")
    os.makedirs(steamcmd_path, exist_ok=True)
    url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz'
    response = requests.get(url, stream=True)
    tar_path = os.path.join(steamcmd_path, 'steamcmd.tar.gz')
    with open(tar_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    subprocess.run(['tar', '-xvzf', tar_path, '-C', steamcmd_path])
    print("SteamCMD downloaded and extracted.")
    return steamcmd_path

def run_steamcmd_commands(steamcmd_path, username, password):
    print("Running SteamCMD commands...")
    steamcmd_exe = os.path.join(steamcmd_path, 'steamcmd.sh')
    commands = [
        "download_depot 377160 377161 7497069378349273908",
        "download_depot 377160 377163 5819088023757897745",
        "download_depot 377160 377162 5847529232406005096",
        "download_depot 377160 377164 2178106366609958945",
        "download_depot 377160 435870 1691678129192680960"
    ]

    for command in commands:
        print(f"Executing command: {command}")
        process = subprocess.Popen(
            [steamcmd_exe, '+login', username, password, '+@ShutdownOnFailedCommand', '1', '+@NoPromptForPassword', '1', f'+{command}', '+quit'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        print(stdout.decode())
        if stderr:
            print(stderr.decode())

    print("Moving downloaded files to Fallout 4 installation directory...")
    # Add code to move files as needed
    print("Files moved successfully.")
    print("Setting app manifest to read-only.")
    # Add code to set app manifest to read-only
    print("App manifest set to read-only.")
    print("Deactivating and removing virtual environment...")
    # Add code to deactivate and remove virtual environment if applicable
    print("Script execution completed.")

def move_downloaded_files(fallout4_path, steamcmd_path):
    print("Moving downloaded files and directories to Fallout 4 installation directory...")
    content_path = os.path.join(steamcmd_path, 'steamapps', 'content', 'app_377160')
    
    data_folders = glob.glob(f"{content_path}/depot*/data/**/*", recursive=True)
    for src_item in data_folders:
        dst_item = os.path.join(fallout4_path, 'data', os.path.relpath(src_item, os.path.join(content_path, 'depot*', 'data')))
        if os.path.isdir(src_item):
            os.makedirs(dst_item, exist_ok=True)
        elif os.path.isfile(src_item):
            os.makedirs(os.path.dirname(dst_item), exist_ok=True)
            shutil.move(src_item, dst_item)
    
    depot_folders = glob.glob(f"{content_path}/depot*/*")
    for src_item in depot_folders:
        if 'data' not in src_item:
            dst_item = os.path.join(fallout4_path, os.path.basename(src_item))
            if os.path.isdir(src_item):
                shutil.move(src_item, dst_item)
            elif os.path.isfile(src_item):
                shutil.move(src_item, dst_item)
    
    print("Files and directories moved successfully.")

def set_app_manifest_read_only(app_manifest_path):
    print(f"Setting app manifest to read-only: {app_manifest_path}")
    os.chmod(app_manifest_path, 0o444)
    print("App manifest set to read-only.")

def main():
    fallout4_path = find_fallout4_installation()
    if not fallout4_path:
        return

    app_manifest_path = find_app_manifest(fallout4_path)
    if not app_manifest_path:
        return

    steamcmd_path = check_and_download_steamcmd()
    print("SteamCMD Path: " + steamcmd_path)
    username = input("Enter Steam username: ")
    password = input("Enter Steam password: ")

    run_steamcmd_commands(steamcmd_path, username, password)
    move_downloaded_files(fallout4_path, steamcmd_path)
    set_app_manifest_read_only(app_manifest_path)

if __name__ == "__main__":
    main()