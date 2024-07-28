import tkinter as tk
import asyncio
import os
import http.client
import urllib.parse
import zipfile
import glob
import shutil
import threading

global root, username, password, steam_guard_code
# Initialize the main application window
root = tk.Tk()
# Have all widgets in the window have a black background and white text
root.configure(bg="black")
root.title("Brapps Fallout 4 Downgrader")
root.geometry("520x180")

# Global variables to store user inputs
username = tk.StringVar()
password = tk.StringVar()
steam_guard_code = tk.StringVar()

def update_status(message):
    def update():
        status_label.config(text=message, bg="black", fg="white", font=("Helvetica", 16))
        root.update_idletasks()
    root.after(0, update)
    
def close_app():
    root.destroy()

def create_welcome_screen():
    global welcome_label, start_button
    welcome_label = tk.Label(root, text="Welcome to the Brapps Fallout 4 Downgrader", bg="black", fg="white", font=("Helvetica", 16))
    welcome_label.pack(pady=20)
    # Button with black background, white text, font size 16, and a white outline/border
    start_button = tk.Button(root, text="Start", command=start_downgrade, bg="grey", fg="white", font=("Helvetica", 16), bd=1, relief='solid')
    start_button.pack(pady=20)

def start_downgrade():
    def run_asyncio():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(scriptpart1())
    
    # Remove welcome message and start button
    welcome_label.pack_forget()
    start_button.pack_forget()
    
    create_status_screen()
    threading.Thread(target=run_asyncio).start()
    
    create_status_screen()
    threading.Thread(target=run_asyncio).start()


def create_credentials_screen():
    # Check if credentials_frame already exists
    if hasattr(root, 'credentials_frame') and root.credentials_frame.winfo_exists():
        return  # Exit if the frame already exists

    root.geometry("520x520")  # Resize window
    status_label.pack_forget()
    status_label.pack(pady=5, anchor='n')  # Move status to top with little padding

    root.credentials_frame = tk.Frame(root, bg="black")
    root.credentials_frame.pack(pady=20)

    global HDActive
    HDActive = tk.IntVar()
    HDTextures = tk.Checkbutton(root.credentials_frame, text="HD Textures", variable=HDActive, fg="#0044FF", bg="black", font=("Helvetica", 12))
    HDTextures.pack(pady=5)
    tk.Label(root.credentials_frame, text="Username:", fg="white", bg="black", font=("Helvetica", 12)).pack(pady=5)
    tk.Entry(root.credentials_frame, textvariable=username, font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root.credentials_frame, text="Password:", fg="white", bg="black", font=("Helvetica", 12)).pack(pady=5)
    tk.Entry(root.credentials_frame, textvariable=password, show="*", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root.credentials_frame, text="Steam Guard Code:", fg="white", bg="black", font=("Helvetica", 12)).pack(pady=5)
    tk.Entry(root.credentials_frame, textvariable=steam_guard_code, font=("Helvetica", 12)).pack(pady=5)
    submit_button = tk.Button(root.credentials_frame, text="Submit", command=lambda: threading.Thread(target=run_scriptpart2).start(), font=("Helvetica", 12))
    submit_button.pack(pady=20)

    def run_scriptpart2():
        asyncio.run(scriptpart2())

def create_final_screen():
    final_label = tk.Label(root, text="Downgrade complete.")
    final_label.pack(pady=20)
    close_button = tk.Button(root, text="Close", command=close_app)
    close_button.pack(pady=20)

def create_status_screen():
    global status_label
    status_label = tk.Label(root, text="", bg="black", fg="white", font=("Helvetica", 16))
    status_label.pack(pady=20)

def find_fallout4_installation():
    global fallout4_path
    root.after(0, lambda: update_status("Searching for Fallout 4 installation..."))
    for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        drive_path = f"{drive}:\\"
        if os.path.exists(drive_path):
            fallout4_paths = glob.glob(f"{drive_path}**/steamapps/common/Fallout 4", recursive=True)
            if fallout4_paths:
                root.after(0, lambda: update_status(f"Fallout 4 found at: {fallout4_paths[0]}"))
                fallout4_path = fallout4_paths[0]
                return fallout4_path
    root.after(0, lambda: update_status("Fallout 4 installation not found."))
    return None

def find_app_manifest(fallout4_path):
    root.after(0, lambda: update_status("Finding app manifest..."))
    steamapps_path = os.path.dirname(os.path.dirname(fallout4_path))
    manifest_path = os.path.join(steamapps_path, 'appmanifest_377160.acf')
    
    if os.path.exists(manifest_path):
        root.after(0, lambda: update_status(f"App manifest found at: {manifest_path}"))
        return manifest_path
    root.after(0, lambda: update_status("App manifest not found."))
    return None

def check_and_download_steamcmd():
    root.after(0, lambda: update_status("Checking and downloading SteamCMD..."))
    steamcmd_path = os.path.join(os.getcwd(), 'steamcmd')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    steamcmd_path = os.path.join(script_dir, 'steamcmd')

    root.after(0, lambda: update_status("Downloading SteamCMD..."))
    os.makedirs(steamcmd_path, exist_ok=True)
    url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'
    parsed_url = urllib.parse.urlparse(url)
    conn = http.client.HTTPSConnection(parsed_url.netloc)
    conn.request("GET", parsed_url.path)
    response = conn.getresponse()
    zip_path = os.path.join(steamcmd_path, 'steamcmd.zip')
    with open(zip_path, 'wb') as f:
        while chunk := response.read(1024):
            f.write(chunk)
    conn.close()
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(steamcmd_path)
    root.after(0, lambda: update_status("SteamCMD downloaded and extracted."))
    return steamcmd_path

async def move_downloaded_files(fallout4_path, steamcmd_path):
    root.after(0, lambda: update_status("Moving downloaded files to installation directory..."))
    content_path = os.path.join(steamcmd_path, 'steamapps', 'content', 'app_377160')
    staging_path = os.path.join(content_path, 'staging')
    
    # Create staging directory
    os.makedirs(staging_path, exist_ok=True)
    
    depot_folders = glob.glob(f"{content_path}/depot*")
    for depot_folder in depot_folders:
        if os.path.isdir(depot_folder):
            for src_item in os.listdir(depot_folder):
                full_src_path = os.path.join(depot_folder, src_item)
                full_dst_path = os.path.join(staging_path, src_item)
                if os.path.isdir(full_src_path):
                    if os.path.exists(full_dst_path):
                        shutil.rmtree(full_dst_path)
                    shutil.move(full_src_path, full_dst_path)
                else:
                    os.makedirs(os.path.dirname(full_dst_path), exist_ok=True)
                    if os.path.exists(full_dst_path):
                        os.remove(full_dst_path)
                    shutil.move(full_src_path, full_dst_path)
            # Remove the empty depot folder
            os.rmdir(depot_folder)
    
    # Move all contents from staging to Fallout 4 directory
    for src_item in os.listdir(staging_path):
        full_src_path = os.path.join(staging_path, src_item)
        full_dst_path = os.path.join(fallout4_path, src_item)
        if os.path.isdir(full_src_path):
            if os.path.exists(full_dst_path):
                shutil.rmtree(full_dst_path)
            shutil.move(full_src_path, full_dst_path)
        else:
            if os.path.exists(full_dst_path):
                os.remove(full_dst_path)
            shutil.move(full_src_path, full_dst_path)
    
    root.after(0, lambda: update_status("Files and directories moved successfully."))

async def set_app_manifest_read_only(app_manifest_path):
    root.after(0, lambda: update_status("Setting app manifest to read-only..."))
    await asyncio.sleep(3)
    os.chmod(app_manifest_path, 0o444)
    root.after(0, lambda: update_status("App manifest set to read-only."))

async def create_steamcmd_script(username, password, steam_guard_code, script_path):
    root.after(0, lambda: update_status("Creating SteamCMD script..."))
    print("login", username, password, steam_guard_code)
    with open(script_path, 'w') as file:
        file.write(f"login {username} {password} {steam_guard_code}\n")
        file.write("download_depot 377160 377162 5847529232406005096\n")
        file.write("download_depot 377160 435870 1691678129192680960\n")
        file.write("download_depot 377160 435871 5106118861901111234\n")
        file.write("download_depot 377160 435880 1255562923187931216\n")
        file.write("download_depot 377160 435882 8482181819175811242\n")
        file.write("download_depot 377160 480630 5527412439359349504\n")
        file.write("download_depot 377160 480631 6588493486198824788\n")
        file.write("download_depot 377160 393885 5000262035721758737\n")
        file.write("download_depot 377160 393895 7677765994120765493\n")
        file.write("download_depot 377160 435881 1207717296920736193\n")
        file.write("download_depot 377160 377164 2178106366609958945\n")
        file.write("download_depot 377160 490650 4873048792354485093\n")
        file.write("download_depot 377160 377161 7497069378349273908\n")
        file.write("download_depot 377160 377163 5819088023757897745\n")
        if (HDActive.get() == 1):
            file.write("download_depot 377160 540810 1558929737289295473\n")
        file.write("quit\n")

async def run_steamcmd_with_script(steamcmd_path, script_path):
    root.after(0, lambda: update_status("Running SteamCMD with script..."))
    asyncio.sleep(4)
    root.after(0, lambda: update_status("This will take a while, go grab a cup of tea."))
    # Place a button temporarily to open the steamapps/content/app_377160 folder in windows explorer
    open_folder_button = tk.Button(root, text="Open folder", command=lambda: threading.Thread(target=open_folder, args=(steamcmd_path,)).start(), font=("Helvetica", 12))
    open_folder_button.pack(pady=20)
    steamcmd_exe = os.path.join(steamcmd_path, 'steamcmd.exe')
    process = await asyncio.create_subprocess_exec(
        steamcmd_exe, f'+runscript {script_path}',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    async def stream_output(stream):
        while True:
            line = await stream.readline()
            if line:
                print(line.decode().strip())
            else:
                break

    await asyncio.gather(
    stream_output(process.stdout),
    stream_output(process.stderr)
    )
        
def open_folder(steamcmd_path):
    os.system(f"start explorer {os.path.join(steamcmd_path, 'steamapps', 'content', 'app_377160')}")

async def scriptpart1():
    fallout4_path = find_fallout4_installation()
    if not fallout4_path:
        root.after(0, lambda: update_status("Fallout 4 installation not found."))
        return
    root.after(0, lambda: update_status(f"Found Fallout 4 installation at \n{fallout4_path}"))
    await asyncio.sleep(2)
    root.after(0, lambda: update_status("Looking for app manifest..."))
    global app_manifest_path
    app_manifest_path = find_app_manifest(fallout4_path)
    if not app_manifest_path:
        root.after(0, lambda: update_status("App manifest not found."))
        return
    root.after(0, lambda: update_status(f"Found app manifest at:\n {app_manifest_path}"))
    root.after(0, create_credentials_screen)

async def deletecreationcontentfiles():
    # Delete the creation club content files found in the fallout 4 directories' data folder. (The ones starting with cc)
    for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        drive_path = f"{drive}:\\"
        if os.path.exists(drive_path):
            fallout4_paths = glob.glob(f"{drive_path}**/steamapps/common/Fallout 4", recursive=True)
            if fallout4_paths:
                for root, dirs, files in os.walk(os.path.join(fallout4_paths[0], "Data")):
                    for file in files:
                        if file.startswith("cc"):
                            os.remove(os.path.join(root, file))
                break

async def scriptpart2():
    steamcmd_path = check_and_download_steamcmd()
    while not username.get() or not password.get():
        await asyncio.sleep(1)
    # Delete the credentials frame
    root.credentials_frame.pack_forget()
    root.geometry("470x150")
    steam_guard = steam_guard_code.get() if steam_guard_code.get() else ""
    print(username.get(), password.get(), steam_guard)
    await asyncio.sleep(5)
    BoolActive = "No"
    if (HDActive.get() == 1):
        BoolActive = "Yes"
    print("HD Textures: " + BoolActive)
    print("Fallout 4 Path: ", fallout4_path)
    print("App Manifest Path: ", app_manifest_path)
    await asyncio.sleep(4)
    await create_steamcmd_script(username.get(), password.get(), steam_guard, os.path.join(steamcmd_path, 'steamcmd_script.txt'))
    await run_steamcmd_with_script(steamcmd_path, os.path.join(steamcmd_path, 'steamcmd_script.txt'))
    await move_downloaded_files(fallout4_path, steamcmd_path)
    await set_app_manifest_read_only(app_manifest_path)
    root.after(0, lambda: update_status("Deleting Creation Club content files..."))
    await deletecreationcontentfiles()
    await asyncio.sleep(2)
    root.after(0, lambda: update_status("Creation Club content files deleted."))
    await asyncio.sleep(3)
    root.after(0, lambda: update_status("You can now close the application."))

create_welcome_screen()
root.mainloop()
