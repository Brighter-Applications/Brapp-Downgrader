# Brapp Downgrader

This is a Downgrader tool for Fallout 4, designed to roll back the game to the previous version before the Bethesda update. 

## Usage

### Windows

1. Download and Extract the downgrader found in the [Releases](https://github.com/Brighter-Applications/Brapp-Downgrader/releases) section.
2. Run the `Downgrade.bat` file, **AS ADMINISTRATOR!** Chocolatey requires admin rights to install packages (such as Python).
3. Follow the on-screen instructions to initiate the downgrade process.

**Please note, this process *will* take a long time, as it involves downloading the previous version of the game. Please be patient and allow the process to complete. If you are anxious about whether the process is working, you can check if the files are downloading in
 ```steamcmd/steamapps/content/app_377160```.
There should slowly be folders appearing in there. If you right-click one of the 'depot' files and check its properties, then check it a few seconds later, you should see the size increasing. Unfortunately, due to the nature of the process, there is no way to show progress in the console.** *:(*

### Linux
1. Download the LINUX downgrader command line script found in the [Releases](https://github.com/Brighter-Applications/Brapp-Downgrader/releases) section.
2. Open a terminal and navigate to the directory where the script is located.
2. run "sudo chmod +x Downgrade.sh" to make the script executable.
3. Run the script with "sudo ./Downgrade.sh"


## Important Note
You may wish to proceed with caution and backup your game files before using this tool. The Downgrader is provided as-is, and the developers are not responsible for any issues that may arise from its use.