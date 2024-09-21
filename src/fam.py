import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)

        # Create a static text to display the information
        self.info_text = wx.StaticText(panel, label="Click a button to see details", pos=(20, 20))

        # Create buttons
        button1 = wx.Button(panel, label="Button 1", pos=(20, 60))
        button2 = wx.Button(panel, label="Button 2", pos=(120, 60))
        button3 = wx.Button(panel, label="Button 3", pos=(220, 60))
        button4 = wx.Button(panel, label="Button 4", pos=(320, 60))

        # Bind buttons to events
        button1.Bind(wx.EVT_BUTTON, self.on_button1_click)
        button2.Bind(wx.EVT_BUTTON, self.on_button2_click)
        button3.Bind(wx.EVT_BUTTON, self.on_button3_click)
        button4.Bind(wx.EVT_BUTTON, self.on_button4_click)

        self.SetTitle("Person Information")
        self.SetSize((450, 200))

    # Event handlers
    def on_button1_click(self, event):
        self.info_text.SetLabel("Name: Mounika, Age: 27, Place: USA")

    def on_button2_click(self, event):
        self.info_text.SetLabel("Name: Pravalika, Age: 24, Place: Hyderabad")

    def on_button3_click(self, event):
        self.info_text.SetLabel("Name: Shriharsha, Age: 23, Place: Vemulawada")

    def on_button4_click(self, event):
        self.info_text.SetLabel("Name: Revanth, Age: 21, Place: Karimnagar")


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None)
        frame.Show(True)
        return True


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
