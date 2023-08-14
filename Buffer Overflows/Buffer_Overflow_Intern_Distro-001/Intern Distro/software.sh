# Software installed for ACE Binex Lecture
# Assuming installation from Lecture template

sudo apt update
sudo apt upgrade -y
sudo apt install -y tasksel ipython3 python3-pip radare2 binutils \
                    libc6:i386 libstdc++6:i386 \
                    libncurses5:i386 gcc-multilib \
                    ghex tree

# Install Python pwntools
pip install pwntools

# Install VScode - Manually install the C/C++ plugin and Python plugin
sudo snap install --classic code

# Install Gnome desktop
sudo tasksel install ubuntu-desktop

echo ""
echo "[+] Please install pwndbg manually (https://github.com/pwndbg/pwndbg)" 
echo "[+] Setup complete! Please reboot for Gnome desktop to work."
echo ""
