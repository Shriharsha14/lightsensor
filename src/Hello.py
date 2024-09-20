import wx

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "Hello Puppy App")
        frame.Show()
        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(300, 200))

        # Panel to hold widgets
        panel = wx.Panel(self)

        # Button
        hello_button = wx.Button(panel, label="Click Me", pos=(100, 50))

        # Event binding: on button click, call self.on_button_click
        hello_button.Bind(wx.EVT_BUTTON, self.on_button_click)

        # Static text to display the message
        self.message = wx.StaticText(panel, label="", pos=(100, 100))

    def on_button_click(self, event):
        # Update the static text to display "Hello Puppy"
        self.message.SetLabel("Hello Puppy")

# Run the application
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
