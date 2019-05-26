import wx
import os
import sys
import wx.lib.agw.gradientbutton as GB
import wx.lib.agw.genericmessagedialog as GMD
import wx.lib.scrolledpanel


class MyPopupMenu(wx.Menu):
    def __init__(self, WinName, parent):
        """
        constructor
        :param WinName: the name of the file that was pressed
        :param parent
        """
        wx.Menu.__init__(self)

        self.WinName = WinName
        self.parent = parent
        # the delete option
        item = wx.MenuItem(self, wx.NewId(), 'Delete file')
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.delete_file, item)
        # the download option
        item = wx.MenuItem(self, wx.NewId(), 'Download')
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.download, item)

    def delete_file(self, event):
        # delete file
        file_name = self.WinName
        self.parent.parent.delete_file(file_name)

    def download(self, event):
        # download file
        filename = self.WinName
        self.onOpenDir(filename)

    def onOpenDir(self, filename):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.DirDialog(
            None, message="Choose a directory",
            defaultPath=self.parent.parent.currentDirectory,
            style=wx.DD_DEFAULT_STYLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            new_dir = str(dlg.GetPath())
            self.parent.parent.get_file(filename, new_dir)
        dlg.Destroy()
