from files_panel import FilesPanel
import wx
from SQL_connection import SQL_connection
import wx.lib.dialogs


class DataServerPage():
    def __init__(self, parent, nb, files):
        self.parent = parent
        self.files = files
        self.PIC_SIZE = self.parent.screenWidth / 9.5
        self.files_panel = FilesPanel(nb, self.set_ending_bmp, self.get_icon,
                                      self.parent.screenWidth, self.parent.screenHeight, True, self.OnButton_Press,
                                      self.files)
        self.files_panel.show_files()

    def set_ending_bmp(self):
        self.data_server_bmp = wx.Bitmap(self.parent.currentDirectory + "\\data_server_icon.png")
        self.data_server_bmp = self.parent.scale_bitmap(self.data_server_bmp, self.PIC_SIZE, self.PIC_SIZE)

    def get_icon(self, ending):
        return self.data_server_bmp

    def OnButton_Press(self, event):
        print "press data server"
        btn = event.GetEventObject()
        data_server_mac = btn.GetLabelText()
        sql_connection_get_data_server_files = SQL_connection(self.parent.db_name)
        sql_connection_get_data_server_files.get_data_server_files(data_server_mac)
        data_server_files = [file_data[1] for file_data in
                             sql_connection_get_data_server_files.get_data_server_files(data_server_mac)]
        print "data_server_files :" + str(data_server_files )
        text = ""
        for file_data in data_server_files:
            print file_data
            username = file_data[:file_data.rfind("$")]
            file_name = file_data[file_data.rfind("$") + 1:file_data.rfind("_", 0,file_data.rfind("_"))] + file_data[file_data.rfind("."):]
            part_index1 = file_data[file_data.rfind("_", 0,file_data.rfind("_")) + 1:file_data.rfind("_")]
            part_index2 = file_data[file_data.rfind("_") + 1:file_data.rfind(".")]
            text += "username: " + username+ "\t" + "file name: " + file_name + "\t"
            if part_index2 != "-1":
                text += " parity of parts: " + part_index1 + "-" + part_index2
            else:
                text += " part: " + part_index1
            text += "\n"
            print text
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self.files_panel, text, "files of data server: " + data_server_mac, size=(self.parent.screenWidth * 0.7, self.parent.screenHeight * 0.7))
        dlg.ShowModal()
        dlg.Destroy()
