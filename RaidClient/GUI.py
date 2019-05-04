import wx
import os
import sys
from SignDialog import SignDialog
#from ClientMain import ClientMain
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

        # self.files = self.client.get_file_list()
        self.files = [r"try.jpg", r"another1.docs", r"fda.txt", r"anereother1.docs", r"fd545a.txt",
                      r"anothe3434r1.png", r"fda.tdf", r"fda.txt", r"fda.py", r"fda.txt", r"fda.ppt", r"fda.xlx",
                      r"fda.txt"]

        self.username = ""
        self.sign()

        self.main_panel = MainPanel(self)

        self.file_panel = FilePanel(self)

        self.file_panel.show_files()

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

    def sign(self):
        dlg = SignDialog(self)
        dlg.ShowModal()
        print "this working:"

    def upload_files(self, files_path):

        print "upload files: " + str(files_path)
        for path in files_path:
            file_name = path[path.rfind("\\") + 1:]
            # result = self.client.upload_file(path)
            result = [True]
            if not result[0]:
                self.fail_msg('could not upload file: ' + file_name)
            else:
                self.files.append(file_name)
                self.file_panel.show_files()

    def delete_file(self, file_name):
        print "delete file: " + str(file_name)
        self.files.remove(file_name)

        self.file_panel.show_files()
        # self.client.delete_file(file_name)
        pass

    def download_file(self, file_name, path_to_save):
        # self.client.set_saving_path(path_to_save)
        # result = self.get_file(file_name)  #[path]
        result = [""]
        print result[0] == ""
        if result[0] == "":
            print "?"
            self.fail_msg('could not retrieve file', )
            # self.client.delete_file(file_name)
            self.files.remove(file_name)
        self.file_panel.show_files()
        print "download file: " + file_name + "  in: " + path_to_save


if __name__ == "__main__":
    app = wx.App(False)

    # client = ClientMain()
    client = ""
    frame = GUI(parent=None, id=-1, title="Test", client=client, app=app)
    frame.Show()

    app.MainLoop()
