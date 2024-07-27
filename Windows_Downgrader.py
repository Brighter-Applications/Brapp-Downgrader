import os
import shutil
import requests
import zipfile
import glob
import asyncio

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
    steamcmd_exe = os.path.join(steamcmd_path, 'steamcmd.exe')

    if os.path.exists(steamcmd_exe):
        print("SteamCMD already exists.")
        return steamcmd_path

    common_paths = [
        os.path.join(os.getenv('ProgramFiles(x86)'), 'SteamCMD'),
        os.path.join(os.getenv('ProgramFiles'), 'SteamCMD'),
        os.path.join(os.getenv('ProgramW6432'), 'SteamCMD')
    ]

    for path in common_paths:
        if os.path.exists(os.path.join(path, 'steamcmd.exe')):
            print(f"SteamCMD found in {path}.")
            return path

    script_dir = os.path.dirname(os.path.abspath(__file__))
    steamcmd_path = os.path.join(script_dir, 'steamcmd')

    print("SteamCMD not found. Downloading SteamCMD...")
    os.makedirs(steamcmd_path, exist_ok=True)
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
    print("steamcmd path: " + steamcmd_path)
    return steamcmd_path

def move_downloaded_files(fallout4_path, steamcmd_path):
    print("Moving downloaded files and directories to Fallout 4 installation directory...")
    content_path = os.path.join(steamcmd_path, 'steamapps', 'content', 'app_377160')
    
    data_folders = glob.glob(f"{content_path}/depot*/data/**/*", recursive=True)
    for src_item in data_folders:
        dst_item = os.path.join(fallout4_path, 'data', os.path.relpath(src_item, os.path.join(content_path, 'depot*', 'data')))
        os.makedirs(os.path.dirname(dst_item), exist_ok=True)
        shutil.move(src_item, dst_item)
    
    depot_folders = glob.glob(f"{content_path}/depot*/*")
    for src_item in depot_folders:
        if 'data' not in os.path.basename(src_item):
            dst_item = os.path.join(fallout4_path, os.path.relpath(src_item, content_path))
            os.makedirs(os.path.dirname(dst_item), exist_ok=True)
            shutil.move(src_item, dst_item)
    
    print("Files and directories moved successfully.")

def set_app_manifest_read_only(app_manifest_path):
    print(f"Setting app manifest to read-only: {app_manifest_path}")
    os.chmod(app_manifest_path, 0o444)
    print("App manifest set to read-only.")

def create_steamcmd_script(username, password, steam_guard_code, script_path):
    with open(script_path, 'w') as file:
        file.write(f"login {username} {password} {steam_guard_code}\n")
        file.write("download_depot 377160 377161 7497069378349273908\n")
        file.write("download_depot 377160 377162 5847529232406005096\n")
        file.write("download_depot 377160 377164 2178106366609958945\n")
        file.write("download_depot 377160 435870 1691678129192680960\n")
        file.write("download_depot 377160 435871 5106118861901111234\n")
        file.write("download_depot 377160 435880 1255562923187931216\n")
        file.write("download_depot 377160 435881 1207717296920736193\n")
        file.write("download_depot 377160 435882 8482181819175811242\n")
        file.write("download_depot 377160 480630 5527412439359349504\n")
        file.write("download_depot 377160 480631 6588493486198824788\n")
        file.write("download_depot 377160 393885 5000262035721758737\n")
        file.write("download_depot 377160 490650 4873048792354485093\n")
        file.write("download_depot 377160 393895 7677765994120765493\n")
        file.write("download_depot 377160 540810 1558929737289295473\n")
        file.write("download_depot 377160 377163 5819088023757897745\n")
        file.write("quit\n")

async def run_steamcmd_with_script(steamcmd_path, script_path):
    steamcmd_exe = os.path.join(steamcmd_path, 'steamcmd.exe')
    process = await asyncio.create_subprocess_exec(
        steamcmd_exe, f'+runscript {script_path}',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()
    print(stdout.decode())
    if stderr:
        print(stderr.decode())

async def main():
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
    steam_guard_code = input("Enter Steam Guard code: ")

    script_path = os.path.join(os.path.dirname(__file__), 'steamcmd_script.txt')
    create_steamcmd_script(username, password, steam_guard_code, script_path)

    await run_steamcmd_with_script(steamcmd_path, script_path)
    move_downloaded_files(fallout4_path, steamcmd_path)
    set_app_manifest_read_only(app_manifest_path)

if __name__ == "__main__":
    asyncio.run(main())