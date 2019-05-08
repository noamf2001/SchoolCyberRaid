import wx
import os
import sys
from SignDialog import SignDialog
# from MainServer import MainServer
from MainPanel import MainPanel
from files_panel import FilePanel
import thread

INSTRUCTION_TEXT = "bleblable\nbery boring text"


class GUI(wx.Frame):

    def __init__(self, parent, id, title, server, app):
        # , init_files
        # First retrieve the screen size of the device
        self.app = app
        screen_size = wx.DisplaySize()
        self.screenWidth = screen_size[0] * 0.9
        self.screenHeight = screen_size[1] * 0.8

        self.color = wx.Colour(117, 194, 229, 255)

        self.server = server

        self.currentDirectory = os.getcwd()

        # Create a frame
        wx.Frame.__init__(self, parent, id, title, size=(self.screenWidth, self.screenHeight),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, pos=(0, 0))

        self.nb = wx.Notebook(self, - 1, style=wx.BK_DEFAULT)



        # self.files = self.client.get_file_list()
        self.files = [r"try.jpg", r"another1.docs", r"fda.txt", r"anereother1.docs", r"fd545a.txt",
                      r"anothe3434r1.png", r"fda.tdf", r"fda.txt", r"fda.py", r"fda.txt", r"fda.ppt", r"fda.xlx",
                      r"fda.txt"]
        for i in range(20):
            self.files.append("num" + str(i) + ".txt")

        self.main_panel = MainPanel(self)

        self.file_panel = FilePanel(self)

        self.file_panel.show_files()


    def add_instruction_page(self):
        instruction = wx.Panel(self, -1)
        wx.StaticText(self, INSTRUCTION_TEXT, -1, style=wx.ALIGN_CENTER)
        self.nb.addPage(instruction, "instructions")

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
    frame = GUI(parent=None, id=-1, title="Test", server=server, app=app)
    frame.Show()

    app.MainLoop()
