import wx
import os
import sys
import wx.lib.agw.gradientbutton as GB
import wx.lib.agw.genericmessagedialog as GMD
import wx.lib.scrolledpanel


class DataServerSettingsRightClickPopup(wx.Menu):
    def __init__(self, parent, add_data_server):
        wx.Menu.__init__(self)
        self.add_data_server = add_data_server
        self.parent = parent
        item = wx.MenuItem(self, wx.NewId(), 'add data server')
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.add_data_server_popup, item)

    def add_data_server_popup(self, event):
        print "add_data_server_popup"
        dlg_ip = wx.TextEntryDialog(
            self.parent, 'please enter ip address',
            'add data server', '')

        ip = ""
        mac = ""
        if dlg_ip.ShowModal() == wx.ID_OK:
            ip = dlg_ip.GetValue()
        dlg_ip.Destroy()
        if ip != "":
            dlg_mac = wx.TextEntryDialog(
                self.parent, 'please enter mac address',
                'add data server', '')
            if dlg_mac.ShowModal() == wx.ID_OK:
                mac = dlg_mac.GetValue()
            dlg_mac.Destroy()
            if mac != "":
                self.add_data_server(ip, mac)
