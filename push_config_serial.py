import netmiko
from tkinter import filedialog as fd

filetypes = (
    ('text files', '*.txt'),
    ('All files', '*.*')
)

com_port = input("Enter COM port number (3):")

if com_port is None:
    com_port = 3

device = {
    "device_type": "cisco_ios_serial",
    "serial_settings": {"port": f"COM{com_port}"},
    "fast_cli": False
}

filename = fd.askopenfilename(title="Select config file to push to console connection", filetypes=filetypes)
serial_conn_handler = netmiko.ConnectHandler(**device)

with open(filename, mode="r") as command_list:
    print(f"{filename} opened successfully.")
    print("Beginning to send commands...")
    for command in command_list:
        print(f"Sending {command.rstrip()}...")
        serial_conn_handler.send_command_timing(command)
        print(f"{command.rstrip()} sent.")
print("All commands sent.  Disconnecting serial connection.")
serial_conn_handler.disconnect()
