import wx
import wx.lib.scrolledpanel


class DataServerSettingsRightClickPopup(wx.Menu):
    def __init__(self, parent, add_data_server):
        """
        constructor
        :param parent:
        :param add_data_server: the function for adding data server
        """
        wx.Menu.__init__(self)
        self.add_data_server = add_data_server
        self.parent = parent
        item = wx.MenuItem(self, wx.NewId(), 'add data server')
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.add_data_server_popup, item)

    def add_data_server_popup(self, event):
        """
        after pressing on right click
        :param event: not needed because a dialog is open - does not need pos or object
        """
        dlg_ip = wx.TextEntryDialog(
            self.parent, 'please enter ip address',
            'add data server', '')

        ip = ""
        mac = ""
        if dlg_ip.ShowModal() == wx.ID_OK:
            ip = dlg_ip.GetValue()
        dlg_ip.Destroy()
        # only if got ip
        if ip != "":
            dlg_mac = wx.TextEntryDialog(
                self.parent, 'please enter mac address',
                'add data server', '')
            if dlg_mac.ShowModal() == wx.ID_OK:
                mac = dlg_mac.GetValue()
            dlg_mac.Destroy()
            # only if got mac
            if mac != "":
                self.add_data_server(ip, mac)
