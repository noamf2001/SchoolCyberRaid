import wx
import os
from SignDialog import SignDialog
from ClientMain import ClientMain
from MainPanel import MainPanel
from Files_Panel import FilePanel
from wx.lib.pubsub import pub
import thread


class GUI(wx.Frame):
    def __init__(self, parent, id, title, app):
        """
        constructor
        the parameters are regular parameters for a frame
        """
        action_call_after_show = {1: self.sign_up_call_after, 2: self.sign_in_call_after,
                                  3: self.upload_file_call_after, 4: self.get_file_call_after,
                                  6: self.get_file_list_call_after,
                                  -1: self.disconnect_call_after}

        self.client = ClientMain(action_call_after_show)
        thread.start_new_thread(self.client.main_recv, ())

        # init_files
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

        # subscribe - to let the client to update the gui
        pub.subscribe(self.upload_file_show_result, "upload_file")

        pub.subscribe(self.sign_in_show_result, "sign_in")

        pub.subscribe(self.sign_up_show_result, "sign_up")

        pub.subscribe(self.get_file_show_result, "get_file")

        pub.subscribe(self.get_files_list_show_result, "get_file_list")

        pub.subscribe(self.disconnect_show_result, "disconnect")

        self.sign()

    def scale_bitmap(self, bitmap, width, height):
        """
        :param bitmap: the img
        :param width:
        :param height:
        :return: the img var - using
        """
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

    def dialog_msg(self, title, msg):
        """
        create a msg to show the client
        dialog parameters
        :param title:
        :param msg:
        """
        dlg = wx.MessageDialog(self, msg,
                               title,
                               wx.OK | wx.ICON_INFORMATION
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

    def start_main_screen(self):
        """
        create main screen after log in
        """
        # self.client.get_file_list()
        self.main_panel = MainPanel(self)
        self.file_panel = FilePanel(self)
        self.file_panel.show_files()

    def sign(self):
        """
        first screen - to sign in\up
        """
        self.dlg = SignDialog(self)
        self.dlg.ShowModal()

    def sign_in_show_result(self, result):
        """
        :param result: the parameters for this action - [boolean]
        """
        if result[0]:
            self.dlg.Destroy()
            self.client.get_file_list()
            self.start_main_screen()
        else:
            self.dialog_msg("FAIL", "could not sign in")

    def sign_in_call_after(self, result):
        """
        call a method that will affect the GUI without stopping an action the GUI does in this moment - user callAfter
        :param result: the parameters to pass to the real method
        """
        wx.CallAfter(pub.sendMessage, "sign_in", result=result)

    def sign_up_show_result(self, result):
        """
        :param result: the parameters for this action - [boolean]
        """
        if result[0]:
            self.dlg.Destroy()
            self.start_main_screen()
        else:
            self.dialog_msg("FAIL", "could not sign up")

    def sign_up_call_after(self, result):
        """
        call a method that will affect the GUI without stopping an action the GUI does in this moment - user callAfter
        :param result: the parameters to pass to the real method
        """
        wx.CallAfter(pub.sendMessage, "sign_up", result=result)

    def upload_file_show_result(self, result):
        """
        :param result: the parameters for this action - [file name, boolean if success]
        """
        file_name = result[0]
        if not result[1]:
            self.dialog_msg("FAIL", 'could not upload file: ' + file_name)
        else:
            self.files.append(file_name)
            self.file_panel.show_files()

    def upload_file_call_after(self, result):
        """
        call a method that will affect the GUI without stopping an action the GUI does in this moment - user callAfter
        :param result: the parameters to pass to the real method
        """
        wx.CallAfter(pub.sendMessage, "upload_file", result=result)

    def upload_files(self, files_path):
        """
        the function that the gui call to upload files
        :param files_path: [file1 - path,file2 - path,...]
        """
        for path in files_path:
            self.client.upload_file(path)

    def get_file_list_call_after(self, result):
        """
        call a method that will affect the GUI without stopping an action the GUI does in this moment - user callAfter
        :param result: the parameters to pass to the real method
        """
        wx.CallAfter(pub.sendMessage, "get_file_list", result=result)

    def get_files_list_show_result(self, result):
        """
        :param result: the parameters for this action - [file 1 name,....]
        """
        self.files = result
        self.file_panel.show_files()

    def delete_file(self, file_name):
        """
        :param file_name: the file to delete
        """
        self.files.remove(file_name)
        self.file_panel.show_files()
        self.client.delete_file(file_name)

    def get_file_show_result(self, result):
        """
        :param result: the parameters for this action - [file name] - file name = "" - did not succeeded
        """
        if result[1] == "":
            self.dialog_msg("FAIL", 'could not retrieve file: ' + result[0])
            self.delete_file(result[0])  # if did not got the file -> delete it
        else:
            self.dialog_msg("SUCCESS", 'the file: ' + result[0] + " is saved")
        self.file_panel.show_files()

    def get_file_call_after(self, result):
        """
        call a method that will affect the GUI without stopping an action the GUI does in this moment - user callAfter
        :param result: the parameters to pass to the real method
        """
        wx.CallAfter(pub.sendMessage, "get_file", result=result)

    def get_file(self, file_name, path_to_save):
        """
        :param file_name: file name
        :param path_to_save: path to download the file to
        """
        # set the next dest of the file
        self.client.set_saving_path(path_to_save)
        self.client.get_file(file_name)

    def disconnect_show_result(self, result):
        """
        :param result: it does not matter
        """
        self.dialog_msg("disconnect", 'the server is disconnect\n'
                                      'or\n'
                                      'this computer has a problem with his internet connection')
        exit()

    def disconnect_call_after(self, result):
        """
        call a method that will affect the GUI without stopping an action the GUI does in this moment - user callAfter
        :param result: the parameters to pass to the real method
        """
        wx.CallAfter(pub.sendMessage, "disconnect", result=result)


if __name__ == "__main__":
    app = wx.App(False)

    frame = GUI(parent=None, id=-1, title="NETWORK - RAID", app=app)
    frame.Show()

    app.MainLoop()
