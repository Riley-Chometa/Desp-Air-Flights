# comp370fall2022

## Installation
One thing to note is that you may have to reboot your system and enable virtualization in your bios, this is different for most systems so you'll have to google "how to enable bios for *insert brand of computer*"
 - This is a web application so installation for the end user will typically be *go to the website*, but we do not have a server that we can host this on for free sadly and these are the installation instructions for setting it up on a developers machine for developement

- [ ] git clone the repo to your local system
- [ ] make sure to check the system requirements for wsl 2 backend here and have everything setup that they describe:
      https://docs.docker.com/desktop/install/windows-install/#wsl-2-backend
- [ ] download the Docker Desktop executable here:
      https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe 
- [ ] run the executable and follow the "Install Interactively" instruction at the following link:
      https://docs.docker.com/desktop/install/windows-install/#install-docker-desktop-on-windows
- [ ] after installation is complete, make sure to read step 5 carefully and follow the instructions given if you are not using an administrator account
- [ ] then follow these instructions to open Docker Desktop:
      https://docs.docker.com/desktop/install/windows-install/#start-docker-desktop
- [ ] after that, if you are prompted with an error about wsl 2 not being enabled, go to the link they provide and follow the instructions to enable it, then restart your pc
- [ ] then, open a command prompt in the root directory of the project
- [ ] run the following command from the terminal:
      docker compose up

      It might take a while to build the containers so dont worry if it seems like its taking a while

      After its done building and the containers are all started, the app should now be available from your browser at the web address: https://localhost:8080
