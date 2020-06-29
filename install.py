import os

pi = 0
while pi !=1 or pi != 2:
    pi = input("Are you on a Pi ? \n1- Yes\n2- No")

print("Install pyQt5")
os.system('sudo apt install python3-pyqt5')

if pi == 1:
    print("Install Libnfc")
    os.system('sudo apt-get install libnfc-bin libnfc-examples libnfc-pn53x-examples')
    print("Install other required python tools")
    os.system('pip3 install -r requirements.txt')
    print("Configuration of Libnfc")
    os.system('sudo cp libnfc.conf /etc/nfc/libnfc.conf')
    print("Install font")
    os.system('mkdir ~/.fonts && cp ~/app/*.ttf ~/.fonts/ && fc-cache -v -f')
    print("Configuration of the start on boot")
    os.system('sudo cp laclef.desktop ~/.config/autostart/laclef.desktop')
    print("Rebooting...")
    os.system('sudo reboot -h 0')


print("Starting the app in test mode")
os.system("python3 start_app.py")
