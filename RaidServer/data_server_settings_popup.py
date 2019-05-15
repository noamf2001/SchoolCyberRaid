import wx
import os
import sys
import wx.lib.agw.gradientbutton as GB
import wx.lib.agw.genericmessagedialog as GMD
import wx.lib.scrolledpanel


class DataServerSettingsPopup(wx.Menu):
    def __init__(self, mac_address, parent, remove_data_server):
        wx.Menu.__init__(self)
        self.remove_data_server = remove_data_server
        self.mac_address = mac_address
        self.parent = parent
        item = wx.MenuItem(self, wx.NewId(), 'remove data server')
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.remove_data_server_popup, item)

    def remove_data_server_popup(self, event):
        # delete file
        self.remove_data_server(self.mac_address)
