from files_panel import FilesPanel
import wx


class DataServerPage():
    def __init__(self, parent, nb, get_data_servers):
        self.parent = parent
        self.PIC_SIZE = self.parent.screenWidth / 11
        self.files_panel = FilesPanel(nb, self.set_ending_bmp, self.get_icon, get_data_servers,
                                      self.parent.screenWidth, self.parent.screenHeight, True,self.OnButton_Press)
        self.files_panel.show_files()

    def set_ending_bmp(self):
        self.data_server_bmp = wx.Bitmap(self.parent.currentDirectory + "\\data_server_icon.png")
        self.data_server_bmp = self.parent.scale_bitmap(self.data_server_bmp, self.PIC_SIZE, self.PIC_SIZE)

    def get_icon(self, ending):
        return self.data_server_bmp

    def OnButton_Press(self, event):
        print "press data server"
        btn = event.GetEventObject()
        data_server_ip = btn.GetLabelText()

