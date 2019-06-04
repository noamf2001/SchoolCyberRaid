from files_panel import FilesPanel
import wx
from SQL_connection import SQL_connection
import wx.lib.dialogs


class DataServerPage:
    def __init__(self, parent, nb, data_servers):
        """
        constructor
        :param parent:
        :param nb: the notebook
        :param data_servers: data servers connected
        """
        self.parent = parent
        self.data_servers = data_servers
        self.PIC_SIZE = self.parent.screenWidth / 9.5  # size of data server icon
        self.files_panel = FilesPanel(nb, self.set_ending_bmp, self.get_icon,
                                      self.parent.screenWidth, self.parent.screenHeight, True, self.OnButton_Press,
                                      self.data_servers)
        self.files_panel.show_files()

    def set_ending_bmp(self):
        """
        set the data server icon instance
        """
        self.data_server_bmp = wx.Bitmap(self.parent.currentDirectory + "\\data_server_icon.png")
        self.data_server_bmp = self.parent.scale_bitmap(self.data_server_bmp, self.PIC_SIZE, self.PIC_SIZE)

    def get_icon(self, ending):
        """
        :param ending: default function for the show files
        :return: the data server bmp - because we have only one option
        """
        return self.data_server_bmp

    def OnButton_Press(self, event):
        """
        after pressing a data server
        :param event: the info about the press
        """
        btn = event.GetEventObject()
        data_server_mac = btn.GetLabelText()
        # get the files that in that data server
        sql_connection_get_data_server_files = SQL_connection(self.parent.db_name)
        data_server_files = [file_data[1] for file_data in
                             sql_connection_get_data_server_files.get_data_server_files(data_server_mac)]
        sql_connection_get_data_server_files.close_sql()
        text = ""
        for file_data in data_server_files:
            username = file_data[:file_data.rfind("$")]
            file_name = file_data[file_data.rfind("$") + 1:file_data.rfind("_", 0, file_data.rfind("_"))] + file_data[
                                                                                                            file_data.rfind(
                                                                                                                "."):]
            part_index1 = file_data[file_data.rfind("_", 0, file_data.rfind("_")) + 1:file_data.rfind("_")]
            part_index2 = file_data[file_data.rfind("_") + 1:file_data.rfind(".")]
            text += "username: " + username + "\t" + "file name: " + file_name + "\t"
            if part_index2 != "-1":
                text += " parity of parts: " + part_index1 + "-" + part_index2
            else:
                text += " part: " + part_index1
            text += "\n"
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self.files_panel, text, "files of data server: " + data_server_mac,
                                                   size=(self.parent.screenWidth * 0.7, self.parent.screenHeight * 0.7))
        dlg.ShowModal()
        dlg.Destroy()
