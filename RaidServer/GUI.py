import wx
import os
import sys
from MainServer import MainServer
# from files_panel import FilesPanel
import thread
from instruction_panel import InstructionPanel
from files_page import FilesPage
from data_server_page import DataServerPage
from data_server_settings_page import DataServerSettingsPage
from wx.lib.pubsub import pub


def dict_delete_by_value(dict, value_del):
    """
    reverse of dict function
    :param dict:
    :param value_del: value to search
    """
    for key, value in dict.items():
        if value == value_del:
            del dict[key]
            break


class GUI(wx.Frame):
    def __init__(self, parent, id, title, app):
        """
        constructor
        :param parent:
        :param id:
        :param title:
        :param app:
        """
        action_call_after_show = {-1: self.disconnect_data_server_call_after, 1: self.sign_up_data_server_call_after,
                                  3: self.upload_file_call_after,
                                  5: self.delete_file_call_after}
        self.app = app
        self.db_name = "db.sqlite"
        #os.remove(self.db_name)
        self.main_server = MainServer(self.db_name, action_call_after_show,
                                      saving_path=r"C:\Users\Sharon\Documents\save_server")
        thread.start_new_thread(self.main_server.main, ())
        screen_size = wx.DisplaySize()
        self.screenWidth = screen_size[0] * 0.9
        self.screenHeight = screen_size[1] * 0.8

        self.currentDirectory = os.getcwd()

        wx.Frame.__init__(self, parent, id=id, title=title, size=(self.screenWidth, self.screenHeight),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        pub.subscribe(self.sign_up_data_server_show_result, "add_data_server")

        pub.subscribe(self.upload_file_show_result, "upload_file")

        pub.subscribe(self.delete_file_show_result, "delete_file")

        pub.subscribe(self.disconnect_data_server_show_result, "disconnect_data_server")

        self.nb = wx.Notebook(self, size=(self.screenWidth, self.screenHeight))
        inst = InstructionPanel(self.nb, self.screenWidth, self.screenHeight)

        self.files_page_files = []
        self.files_page_users_files = {}
        self.files_page = FilesPage(self, self.nb, self.files_page_files,
                                    self.files_page_users_files)  # self.main_server.files)

        self.data_servers_settings_page = DataServerSettingsPage(self, self.nb,
                                                                 self.main_server.optional_data_server.values())  # self.main_server.get_data_server()

        self.data_servers_page_files = []
        self.data_servers_page = DataServerPage(self, self.nb,
                                                self.data_servers_page_files)  # self.main_server.get_data_server()

        self.nb.AddPage(self.data_servers_page.files_panel, "data servers")
        self.nb.AddPage(self.files_page.files_panel, "files")
        self.nb.AddPage(self.data_servers_settings_page.files_panel, "data servers settings")
        self.nb.AddPage(inst, "About")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def data_server_settings_show_result(self):
        """
        after changing the data server list - update it on screen
        """
        self.data_servers_settings_page.data_servers = self.main_server.optional_data_server.values()
        self.data_servers_settings_page.files_panel.show_files()

    def remove_data_server(self, mac_address):
        """
        remove data server so it will not be legal
        :param mac_address: the identifier
        """
        # disconnect from it if it is connected
        if mac_address in self.main_server.connected_data_server.keys():
            self.main_server.command_result_data_server.put([self.main_server.connected_data_server[mac_address], [-1, []]])
        dict_delete_by_value(self.main_server.optional_data_server, mac_address)
        self.data_server_settings_show_result()

    def add_data_server(self, ip_address, mac_address):
        """
        add data server to be legal to connect to
        :param ip_address: identifier
        :param mac_address: identifier
        """
        self.main_server.optional_data_server[ip_address] = mac_address
        self.data_server_settings_show_result()

    def sign_up_data_server_show_result(self, result):
        """
        show on GUI that a data server connected
        :param result: mac address
        """
        self.data_servers_page_files.append(result)
        self.data_servers_page.files_panel.show_files()

    def sign_up_data_server_call_after(self, result):
        """
        tell the GUI that a new data server connect from main server without interrupting
        :param result: mac address
        """
        wx.CallAfter(pub.sendMessage, "add_data_server", result=result)

    def disconnect_data_server_show_result(self, result):
        """
        show on GUI that a data server is disconnecting
        :param result: mac address
        """
        self.data_servers_page_files.remove(result)
        self.data_servers_page.files_panel.show_files()

    def disconnect_data_server_call_after(self, result):
        """
        tell the GUI that a new data server disconnect from main server without interrupting
        :param result: mac address
        """
        wx.CallAfter(pub.sendMessage, "disconnect_data_server", result=result)

    def upload_file_show_result(self, result):
        """
        show on GUI that a new file was upload
        :param result:
        """
        username = result[:result.rfind("$")]
        file_name = result[result.rfind("$") + 1:]
        self.files_page_users_files[file_name] = username
        self.files_page_files.append(file_name)
        self.files_page.files_panel.show_files()

    def upload_file_call_after(self, result):
        """
        tell the GUI that a new file is being upload from client, so call the GUI to put it, without interrupting GUI action
        :param result: file name
        """
        wx.CallAfter(pub.sendMessage, "upload_file", result=result)

    def delete_file_show_result(self, result):
        """
        delete the file from the files page
        :param result: file name
        """
        username = result[:result.rfind("$")]
        file_name = result[result.rfind("$") + 1:]
        # on the screen, we show the file name without the username, but in the server we use: usename$filenmae
        del self.files_page_users_files[file_name]
        self.files_page_files.remove(file_name)
        self.files_page.files_panel.show_files()

    def delete_file_call_after(self, result):
        """
        tell the GUI that a new file is being delete , so call the GUI to put it, without interrupting GUI action
        :param result: file name
        """
        wx.CallAfter(pub.sendMessage, "delete_file", result=result)

    def scale_bitmap(self, bitmap, width, height):
        """
        build the bitmap instance by the parameters
        :param bitmap:
        :param width:
        :param height:
        :return: bitmap instance
        """
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

    def fail_msg(self, msg):
        """
        open dialog for client of FAIL title
        :param msg: the msg to show - reason
        """
        dlg = wx.MessageDialog(self, msg,
                               'Fail',
                               wx.OK | wx.ICON_INFORMATION
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    frame = GUI(parent=None, id=-1, title="admin-GUI", app=app)
    frame.Show()

    app.MainLoop()
