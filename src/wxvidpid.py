import wx
import serial
import time
import serial.tools.list_ports

class SerialApp(wx.Frame):
    def __init__(self, parent, title):
        super(SerialApp, self).__init__(parent, title=title, size=(500, 300))

        # Create the main panel and layout
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # DropBox (ComboBox) for COM ports
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.port_label = wx.StaticText(panel, label="COM Port:")
        hbox1.Add(self.port_label, flag=wx.RIGHT, border=8)
        
        self.combobox = wx.ComboBox(panel)
        hbox1.Add(self.combobox, proportion=1)
        self.search_button = wx.Button(panel, label="Search")
        hbox1.Add(self.search_button, flag=wx.LEFT, border=8)
        
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Connect/Disconnect buttons
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.connect_button = wx.Button(panel, label="Connect")
        hbox2.Add(self.connect_button, flag=wx.RIGHT, border=8)
        self.disconnect_button = wx.Button(panel, label="Disconnect")
        hbox2.Add(self.disconnect_button, flag=wx.RIGHT, border=8)
        
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Log area to show device responses
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.log_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        hbox3.Add(self.log_area, proportion=1, flag=wx.EXPAND)
        
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)

        # Buttons for read commands (Read SN and Version)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.sn_button = wx.Button(panel, label="Read SN")
        hbox4.Add(self.sn_button, flag=wx.RIGHT, border=8)
        self.version_button = wx.Button(panel, label="Read Version")
        hbox4.Add(self.version_button, flag=wx.RIGHT, border=8)
        
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        # Bind the button events to their handlers
        self.search_button.Bind(wx.EVT_BUTTON, self.on_search)
        self.connect_button.Bind(wx.EVT_BUTTON, self.on_connect)
        self.disconnect_button.Bind(wx.EVT_BUTTON, self.on_disconnect)
        self.sn_button.Bind(wx.EVT_BUTTON, self.read_sn)
        self.version_button.Bind(wx.EVT_BUTTON, self.read_version)

        # Serial port object and status
        self.ser = None
        self.connected = False

        self.Show()

    def on_search(self, event):
        """Search for available COM ports based on VID:PID."""
        usb_hwid_str = ["USB VID:PID=045E:0646"]
        ports = self.list_com_ports(usb_hwid_str)
        self.combobox.Clear()
        self.combobox.AppendItems(ports)
        if ports:
            self.log_area.AppendText("Available COM ports: " + ", ".join(ports) + "\n")
        else:
            self.log_area.AppendText("No COM ports found matching VID:PID.\n")

    def on_connect(self, event):
        """Connect to the selected COM port."""
        port = self.combobox.GetValue()
        if port:
            self.ser = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Wait for connection
            if self.ser.is_open:
                self.log_area.AppendText(f"Connected to {port}\n")
                self.connected = True
            else:
                self.log_area.AppendText(f"Failed to connect to {port}\n")

    def on_disconnect(self, event):
        """Disconnect from the serial port."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.log_area.AppendText("Serial port closed.\n")
            self.connected = False

    def read_sn(self, event):
        """Read the serial number."""
        if self.connected and self.ser:
            self.send_command('sn\r\n', "Serial Number")

    def read_version(self, event):
        """Read the version."""
        if self.connected and self.ser:
            self.send_command('version\r\n', "Version")

    def send_command(self, command, label):
        """Send a command and log the response."""
        self.ser.write(command.encode())
        time.sleep(1)
        if self.ser.in_waiting > 0:
            response = self.ser.read(self.ser.in_waiting).decode('utf-8')
            self.log_area.AppendText(f"{label}: {response}\n")
        else:
            self.log_area.AppendText(f"No response for {label}.\n")

    def list_com_ports(self, usb_hwid_str):
        """List available COM ports that match the given VID:PID."""
        ports = []
        for port_info in serial.tools.list_ports.comports():
            if any(hwid in port_info.hwid for hwid in usb_hwid_str):
                ports.append(port_info.device)
        return ports

# Main function to run the wxPython app
def main():
    app = wx.App(False)
    frame = SerialApp(None, "Serial Communication App")
    app.MainLoop()

if __name__ == "__main__":
    main()
