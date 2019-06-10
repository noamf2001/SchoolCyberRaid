import wx
import wx.lib.scrolledpanel


class DataServerSettingsPopup(wx.Menu):
    def __init__(self, mac_address, parent, remove_data_server):
        """
        constructor
        :param mac_address: the full mac address of the menu
        :param parent:
        :param remove_data_server: function to call when needed
        """
        wx.Menu.__init__(self)
        self.remove_data_server = remove_data_server
        self.mac_address = mac_address
        self.parent = parent
        item = wx.MenuItem(self, wx.NewId(), 'remove data server')
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.remove_data_server_popup, item)

    def remove_data_server_popup(self, event):
        """
        after pressing data server remove
        :param event: not needed
        """
        # delete file
        self.remove_data_server(self.mac_address)
