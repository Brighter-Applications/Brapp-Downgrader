#!/bin/bash

# Download SteamCMD
wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
tar -xvzf steamcmd_linux.tar.gz

#!/bin/bash

# Function to search for a directory
search_directory() {
    local dir_name=$1
    find / -type d -name "$dir_name" 2>/dev/null | head -n 1
}

# Search for the Fallout 4 directory
fallout4_dir=$(search_directory "Fallout 4")

if [ -z "$fallout4_dir" ]; then
    echo "Fallout 4 directory not found."
    exit 1
else
    echo "Fallout 4 directory found at: $fallout4_dir"
fi

if read -p "Do you have the High Definition DLC installed? (Y/N): " -n 1 -r; then
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        HDDLC=true
    fi
fi
# Prompt user for login details
read -p -r "Enter your Steam username: " username
read -s -p -r "Enter your Steam password: " password
echo
read -p -r "Enter your Steam Guard code: " steamguardcode



# Create the script file
{
    echo "login $username $password $steamguardcode"
    echo "download_depot 377160 377162 5847529232406005096"
    echo "download_depot 377160 435870 1691678129192680960"
    echo "download_depot 377160 435871 5106118861901111234"
    echo "download_depot 377160 435880 1255562923187931216"
    echo "download_depot 377160 435882 8482181819175811242"
    echo "download_depot 377160 480630 5527412439359349504"
    echo "download_depot 377160 480631 6588493486198824788"
    echo "download_depot 377160 393885 5000262035721758737"
    echo "download_depot 377160 393895 7677765994120765493"
    echo "download_depot 377160 435881 1207717296920736193"
    echo "download_depot 377160 377164 2178106366609958945"
    echo "download_depot 377160 490650 4873048792354485093"
    echo "download_depot 377160 377161 7497069378349273908"
    if [ $HDDLC ]; then
        echo "download_depot 377160 377163 5819088023757897745"
    fi
    echo "quit"
} > steam_script.txt

# Run SteamCMD with the script file
./steamcmd.sh +runscript steam_script.txt

# Assume the app_377160 directory is in the steamcmd/steamapps/content/ folder
app_377160_dir="./steamcmd/steamapps/content/app_377160"

if [ ! -d "$app_377160_dir" ]; then
    echo "app_377160 directory not found in steamcmd/steamapps/content/."
    exit 1
else
    app_377160_dir=$(realpath "$app_377160_dir")
    echo "app_377160 directory found at: $app_377160_dir"
fi

# Move contents of each folder in app_377160 to the Fallout 4 directory, preserving subfolders
echo "Moving contents of each folder in $app_377160_dir to $fallout4_dir"
for dir in "$app_377160_dir"/*; do
    if [ -d "$dir" ]; then
        cp -r "$dir"/* "$fallout4_dir"
    fi
done

echo "Contents moved successfully."