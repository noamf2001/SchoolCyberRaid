import wx
import os
from SignDialog import SignDialog
from ClientMain import ClientMain
from MainPanel import MainPanel
from files_panel import FilePanel
from wx.lib.pubsub import pub
import thread


class GUI(wx.Frame):

    def __init__(self, parent, id, title, app):
        action_call_after_show = {1: self.sign_up_call_after, 2: self.sign_in_call_after,
                                  3: self.upload_file_call_after, 4: self.get_file_call_after,
                                  6: self.get_file_list_call_after,
                                  -1: self.disconnect_call_after}

        self.client = ClientMain(action_call_after_show)
        thread.start_new_thread(self.client.main_recv, ())

        # , init_files
        # First retrieve the screen size of the device
        self.app = app
        screen_size = wx.DisplaySize()
        self.screenWidth = screen_size[0] * 0.9
        self.screenHeight = screen_size[1] * 0.8

        self.color = wx.Colour(117, 194, 229, 255)

        self.currentDirectory = os.getcwd()

        # Create a frame
        wx.Frame.__init__(self, parent, id, title, size=(self.screenWidth, self.screenHeight),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        self.files = []

        self.username = ""

        pub.subscribe(self.upload_file_show_result, "upload_file")

        pub.subscribe(self.sign_in_show_result, "sign_in")

        pub.subscribe(self.sign_up_show_result, "sign_up")

        pub.subscribe(self.get_file_show_result, "get_file")

        pub.subscribe(self.get_files_list_show_result, "get_file_list")
        pub.subscribe(self.get_files_list_show_result, "disconnect")
        self.sign()

    def scale_bitmap(self, bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

    def dialog_msg(self, title, msg):
        dlg = wx.MessageDialog(self, msg,
                               title,
                               wx.OK | wx.ICON_INFORMATION
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

    def start_main_screen(self):
        # self.client.get_file_list()
        self.main_panel = MainPanel(self)
        self.file_panel = FilePanel(self)

        self.file_panel.show_files()

    def sign(self):
        self.dlg = SignDialog(self)
        self.dlg.ShowModal()

    def sign_in_show_result(self, result):
        print "in: sign_in_show_result: " + str(result)
        if result[0]:
            self.dlg.Destroy()
            self.client.get_file_list()
            self.start_main_screen()
        else:
            self.dialog_msg("FAIL", "could not sign in")

    def sign_in_call_after(self, result):
        print "sign_in_call_after"
        wx.CallAfter(pub.sendMessage, "sign_in", result=result)

    def sign_up_show_result(self, result):
        print "in: sign_up_show_result: " + str(result)
        if result[0]:
            self.dlg.Destroy()
            self.start_main_screen()
        else:
            self.dialog_msg("FAIL", "could not sign up")

    def sign_up_call_after(self, result):
        print "sign_up_call_after"
        wx.CallAfter(pub.sendMessage, "sign_up", result=result)

    def upload_file_show_result(self, result):
        print "in upload_file_show_result: " + str(result)
        file_name = result[0]
        if not result[1]:
            self.dialog_msg("FAIL", 'could not upload file: ' + file_name)
        else:
            self.files.append(file_name)
            self.file_panel.show_files()

    def upload_file_call_after(self, result):
        wx.CallAfter(pub.sendMessage, "upload_file", result=result)

    def upload_files(self, files_path):
        print "upload files: " + str(files_path)
        for path in files_path:
            self.client.upload_file(path)

    def get_file_list_call_after(self, result):
        wx.CallAfter(pub.sendMessage, "get_file_list", result=result)

    def get_files_list_show_result(self, result):
        print "get_files_list_show_result: " + str(result)
        self.files = result
        self.file_panel.show_files()

    def delete_file(self, file_name):
        print "delete file: " + str(file_name)
        self.files.remove(file_name)
        self.file_panel.show_files()
        self.client.delete_file(file_name)

    def get_file_show_result(self, result):
        print "get_file_show_result: " + str(result[0])
        if result[1] == "":
            self.dialog_msg("FAIL", 'could not retrieve file: ' + result[0])
            self.delete_file(result[0])
        else:
            self.dialog_msg("SUCCESS", 'the file: ' + result[0] + " is saved")
        self.file_panel.show_files()

    def get_file_call_after(self, result):
        print "get_file_call_after"
        wx.CallAfter(pub.sendMessage, "get_file", result=result)

    def get_file(self, file_name, path_to_save):
        self.client.set_saving_path(path_to_save)
        self.client.get_file(file_name)

    def disconnect_show_result(self):
        print "start disconnect"
        self.dialog_msg("disconnect", 'the server is disconnect\n'
                                      'or\n'
                                      'this computer has a problem with his internet connection')
        exit()

    def disconnect_call_after(self):
        wx.CallAfter(pub.sendMessage, "disconnect")


if __name__ == "__main__":
    app = wx.App(False)

    frame = GUI(parent=None, id=-1, title="Test", app=app)
    frame.Show()

    app.MainLoop()
