import wx
import os
import sys
from SignDialog import SignDialog


class GUI(wx.Frame):

    def __init__(self, parent, id, title, client, app):
        # , init_files
        # First retrieve the screen size of the device
        self.app = app
        screen_size = wx.DisplaySize()
        self.screenWidth = screen_size[0] * 0.8
        self.screenHeight = (screen_size[1] - 40) * 0.8
        self.color = wx.Colour(117, 194, 229, 255)

        self.client = client

        self.currentDirectory = os.getcwd()

        # Create a frame
        wx.Frame.__init__(self, parent, id, title, size=(self.screenWidth, self.screenHeight),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, pos=(0, 0))

        self.username = ""
        self.dlg = SignDialog(self)
        self.dlg.ShowModal()

        #####


if __name__ == "__main__":
    app = wx.App(False)

    com = "hi"  # client_com.client_com('127.0.0.1',1000, uuid.uuid4())

    frame = GUI(parent=None, id=-1, title="Test", client=com, app=app)
    frame.Show()

    app.MainLoop()
