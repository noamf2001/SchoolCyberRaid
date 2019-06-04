from files_panel import FilesPanel
import wx
from data_server_settings_right_click_popup import DataServerSettingsRightClickPopup
from data_server_settings_popup import DataServerSettingsPopup


class DataServerSettingsPage:
    def __init__(self, parent, nb, data_servers):
        """
        constructor
        :param parent:
        :param nb: notebook
        :param data_servers:
        """
        self.parent = parent
        self.data_servers = data_servers
        self.PIC_SIZE = self.parent.screenWidth / 9.5  # data srever icon size

        self.files_panel = FilesPanel(nb, self.set_ending_bmp, self.get_icon,
                                      self.parent.screenWidth, self.parent.screenHeight * 0.8, True,
                                      self.OnButton_Press, self.data_servers, self.parent.screenHeight * 0.2,
                                      self.right_click_press)
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
        menu = DataServerSettingsPopup(btn.GetLabelText(), self.files_panel, self.parent.remove_data_server)
        self.files_panel.PopupMenu(menu, (btn.GetPosition()[0] + 80, btn.GetPosition()[1] + 60))
        menu.Destroy()

    def right_click_press(self, event):
        """
        after pressing right click on screen
        :param event:
        """
        btn = event.GetEventObject()
        menu = DataServerSettingsRightClickPopup(self.files_panel, self.parent.add_data_server)
        self.files_panel.PopupMenu(menu, (btn.GetPosition()[0] + 80, btn.GetPosition()[1] + 60))
        menu.Destroy()
