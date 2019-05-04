import wx
import os
import sys
from SignDialog import SignDialog
from ClientMain import ClientMain
from MainPanel import MainPanel
from files_panel import FilePanel


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

        self.init_files = []

        self.username = ""
        self.sign()

        #cSizer = wx.BoxSizer(wx.VERTICAL)

        self.main_panel = MainPanel(self)


        self.file_panel = FilePanel(self)

        #pub.subscribe(self.handle_new_file_lst, "showfiles")


        #pub.subscribe(self.myListener, "open_main_frame")
        #pub.subscribe(self.myListener2, "filelist")
        #pub.subscribe(self.myListener3, "files")
        #pub.subscribe(self.download, "sentfile")

        #self.SetSizer(cSizer)

    def sign(self):
        dlg = SignDialog(self)
        dlg.ShowModal()
        print "this working:"


if __name__ == "__main__":
    app = wx.App(False)

    # client = ClientMain()
    client = ""
    frame = GUI(parent=None, id=-1, title="Test", client=client, app=app)
    frame.Show()

    app.MainLoop()
