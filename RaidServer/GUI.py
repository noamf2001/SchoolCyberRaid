import wx
import os
import sys
# from MainServer import MainServer
from files_panel import FilePanel
import thread
from instructionpanel import InstructionPanel



class GUI(wx.Frame):
    def __init__(self, parent, id, main_server, title, app):
        self.app = app
        self.main_server = main_server

        screen_size = wx.DisplaySize()
        self.screenWidth = screen_size[0] * 0.9
        self.screenHeight = screen_size[1] * 0.8

        wx.Frame.__init__(self, parent, id=id, title=title, size=(self.screenWidth, self.screenHeight),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        # Here we create a panel and a notebook on the panel
        self.nb = wx.Notebook(self,size=(self.screenWidth, self.screenHeight))
        a = InstructionPanel(self.nb)
        self.nb.AddPage(a, "Instructions")
        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def scale_bitmap(self, bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

    def fail_msg(self, msg):
        dlg = wx.MessageDialog(self, msg,
                               'Fail',
                               wx.OK | wx.ICON_INFORMATION
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == "__main__":
    app = wx.App(False)

    # client = ClientMain()
    # server = MainServer()
    # thread.start_new_thread(server.main, ())
    server = ""
    frame = GUI(parent=None, id=-1, title="Test", main_server=server, app=app)
    frame.Show()

    app.MainLoop()
