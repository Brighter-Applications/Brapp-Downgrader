import os
import shutil
import subprocess
import requests
import zipfile
from tqdm import tqdm
import glob

def find_fallout4_installation():
    print("Searching for Fallout 4 installation...")
    for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        drive_path = f"{drive}:\\"
        if os.path.exists(drive_path):
            fallout4_paths = glob.glob(f"{drive_path}**/steamapps/common/Fallout 4", recursive=True)
            if fallout4_paths:
                print(f"Fallout 4 found at: {fallout4_paths[0]}")
                return fallout4_paths[0]
    print("Fallout 4 installation not found.")
    return None

def find_app_manifest(fallout4_path):
    print("Searching for Steam app manifest...")
    # Correct the path to point to the parent directory of 'common'
    steamapps_path = os.path.dirname(os.path.dirname(fallout4_path))
    manifest_path = os.path.join(steamapps_path, 'appmanifest_377160.acf')
    
    # Debugging prints
    print(f"Fallout 4 path: {fallout4_path}")
    print(f"Steamapps path: {steamapps_path}")
    print(f"Manifest path: {manifest_path}")
    
    if os.path.exists(manifest_path):
        print(f"App manifest found at: {manifest_path}")
        return manifest_path
    print("App manifest not found.")
    return None

def check_and_download_steamcmd():
    print("Checking for SteamCMD...")
    steamcmd_path = os.path.join(os.getcwd(), 'steamcmd')
    if not os.path.exists(steamcmd_path):
        print("SteamCMD not found. Downloading SteamCMD...")
        os.makedirs(steamcmd_path)
        url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'
        response = requests.get(url, stream=True)
        zip_path = os.path.join(steamcmd_path, 'steamcmd.zip')
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(steamcmd_path)
        print("SteamCMD downloaded and extracted.")
    else:
        print("SteamCMD already exists.")
    return steamcmd_path

def run_steamcmd_commands(steamcmd_path, username, password):
    print("Running SteamCMD commands...")
    steamcmd_exe = os.path.join(steamcmd_path, 'steamcmd.exe')
    commands = [
        "download_depot 377160 377161 7497069378349273908",
        "download_depot 377160 377163 5819088023757897745",
        "download_depot 377160 377162 5847529232406005096",
        "download_depot 377160 377164 2178106366609958945",
        "download_depot 377160 435870 1691678129192680960",
        "download_depot 377160 435871 5106118861901111234",
        "download_depot 377160 435880 1255562923187931216",
        "download_depot 377160 435881 1207717296920736193",
        "download_depot 377160 435882 8482181819175811242",
        "download_depot 377160 480630 5527412439359349504",
        "download_depot 377160 480631 6588493486198824788",
        "download_depot 377160 393885 5000262035721758737",
        "download_depot 377160 490650 4873048792354485093",
        "download_depot 377160 393895 7677765994120765493",
        "download_depot 377160 540810 1558929737289295473"
    ]
    for command in commands:
        print(f"Executing command: {command}")
        process = subprocess.Popen([steamcmd_exe, '+login', username, password, '+', command, '+quit'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in tqdm(process.stdout):
            print(line.decode(), end='')

def move_downloaded_files(fallout4_path):
    print("Moving downloaded files to Fallout 4 installation directory...")
    content_path = r'C:\Program Files (x86)\Steam\Steamapps\content\app_377160'
    downloaded_files = glob.glob(f"{content_path}/**/*", recursive=True)
    for src_file in downloaded_files:
        if os.path.isfile(src_file):
            dst_file = os.path.join(fallout4_path, os.path.relpath(src_file, content_path))
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.move(src_file, dst_file)
    print("Files moved successfully.")

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

    username = input("Enter Steam username: ")
    password = input("Enter Steam password: ")

    run_steamcmd_commands(steamcmd_path, username, password)
    move_downloaded_files(fallout4_path)
    set_app_manifest_read_only(app_manifest_path)

if __name__ == "__main__":
    main()