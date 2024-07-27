import glob
import os
import shutil
import subprocess
import sys
import requests

def find_fallout4_installation():
    print("Searching for Fallout 4 installation...")
    home_dir = os.getenv('HOME')
    steam_paths = [
        os.path.join(home_dir, ".steam/steam/steamapps/common/Fallout 4"),
        os.path.join(home_dir, ".local/share/Steam/steamapps/common/Fallout 4"),
        os.path.join(home_dir, ".var/app/com.valvesoftware.Steam/.steam/steam/steamapps/common/Fallout 4"),
        "/snap/steam/common/.local/share/steam"
    ]
    for path in steam_paths:
        if os.path.exists(path):
            print(f"Fallout 4 found at: {path}")
            return path
    return None

def find_app_manifest(fallout4_path):
    print("Searching for Steam app manifest...")
    steamapps_path = os.path.dirname(os.path.dirname(fallout4_path))
    manifest_path = os.path.join(steamapps_path, 'appmanifest_377160.acf')
    
    print(f"Fallout 4 path: {fallout4_path}")
    print(f"Steamapps path: {steamapps_path}")
    print(f"Manifest path: {manifest_path}")
    
    if os.path.exists(manifest_path):
        print(f"App manifest found at: {manifest_path}")
        return manifest_path
    print("App manifest not found.")
    return None

def check_and_download_steamcmd():
#    print("Checking for SteamCMD...")
#    steamcmd_exe = shutil.which('steamcmd')
#    steamcmd_path = os.path.dirname(steamcmd_exe) if steamcmd_exe else None
#    if steamcmd_path:
#        print("SteamCMD already exists.")
#        return steamcmd_path

    script_dir = os.path.dirname(os.path.abspath(__file__))
    steamcmd_path = os.path.join(script_dir, 'steamcmd')
    if os.path.exists(steamcmd_path):
        print("SteamCMD already downloaded.")
        return steamcmd_path

    print("SteamCMD not found. Downloading SteamCMD...")
    os.makedirs(steamcmd_path, exist_ok=True)
    url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz'
    response = requests.get(url, stream=True)
    tar_path = os.path.join(script_dir, 'steamcmd_linux.tar.gz')
    with open(tar_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    subprocess.run(['tar', '-xvzf', tar_path, '-C', steamcmd_path])
    print("SteamCMD downloaded and extracted.")
    return steamcmd_path

def move_downloaded_files(fallout4_path, steamcmd_path):
    print("Moving downloaded files and directories to Fallout 4 installation directory...")
    content_path = os.path.join(steamcmd_path, 'steamapps', 'content', 'app_377160')
    
    data_folders = glob.glob(f"{content_path}/depot*/data/**/*", recursive=True)
    for src_item in data_folders:
        if os.path.isdir(src_item):
            dst_item = os.path.join(fallout4_path, 'data', os.path.relpath(src_item, os.path.join(content_path, 'depot*', 'data')))
            os.makedirs(dst_item, exist_ok=True)
        elif os.path.isfile(src_item):
            dst_item = os.path.join(fallout4_path, 'data', os.path.relpath(src_item, os.path.join(content_path, 'depot*', 'data')))
            os.makedirs(os.path.dirname(dst_item), exist_ok=True)
            shutil.move(src_item, dst_item)
    
    depot_folders = glob.glob(f"{content_path}/depot*/*")
    for src_item in depot_folders:
        if 'data' not in os.path.basename(src_item):
            dst_item = os.path.join(fallout4_path, os.path.relpath(src_item, content_path))
            if os.path.isdir(src_item):
                os.makedirs(dst_item, exist_ok=True)
                shutil.move(src_item, dst_item)
            elif os.path.isfile(src_item):
                os.makedirs(os.path.dirname(dst_item), exist_ok=True)
                shutil.move(src_item, dst_item)
    
    print("Files and directories moved successfully.")

def set_app_manifest_read_only(app_manifest_path):
    print(f"Setting app manifest to read-only: {app_manifest_path}")
    os.chmod(app_manifest_path, 0o444)
    print("App manifest set to read-only.")

def run_steamcmd(steamcmd_path, username):
# TODO: detect installed steamcmd download path ($HOME/.local/share/Steam/steamcmd/ on test machine)
# but could be any of the variations of the Steam install path at the top
#    steamcmd_exe = os.path.join(steamcmd_path, 'steamcmd')
#    if not os.path.exists(steamcmd_exe):
#        steamcmd_exe = os.path.join(steamcmd_path, 'steamcmd.sh')
    steamcmd_exe = os.path.join(steamcmd_path, 'steamcmd.sh')

    steamcmd_script = os.path.join(os.getcwd(), 'steamcmd_script.txt')
    process = subprocess.Popen([steamcmd_exe, '+force_download_dir', steamcmd_path, '+login', username, '+runscript', steamcmd_script])
    process.wait()
    print("SteamCMD process has finished.")

def main():
    if os.geteuid() == 0:
        print("Please do not run this script as root.")
        sys.exit(1)

    fallout4_path = find_fallout4_installation()
    if not fallout4_path:
        return

    app_manifest_path = find_app_manifest(fallout4_path)
    if not app_manifest_path:
        return

    steamcmd_path = check_and_download_steamcmd()
    print("steamcmd path: " + steamcmd_path)
    username = input("Enter Steam username: ")
    run_steamcmd(steamcmd_path, username)

    move_downloaded_files(fallout4_path, steamcmd_path)
    set_app_manifest_read_only(app_manifest_path)

if __name__ == "__main__":
    main()