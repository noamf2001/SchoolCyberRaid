import wx
import os
import sys
import wx.lib.agw.gradientbutton as GB
import wx.lib.agw.genericmessagedialog as GMD
import wx.lib.scrolledpanel


class MyPopupMenu(wx.Menu):
    def __init__(self, WinName, parent):
        wx.Menu.__init__(self)

        self.WinName = WinName
        self.parent = parent
        item = wx.MenuItem(self, wx.NewId(), 'Delete file')
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.delete_file, item)

        item = wx.MenuItem(self, wx.NewId(), 'Download')
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.download, item)


    def delete_file(self, event):
        print "delete file press"
        # delete file
        file_name = self.WinName
        print "file name: " + file_name
        self.parent.parent.delete_file(file_name)


    def download(self, event):
        # download file
        print "starting download in GUI"
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
            self.parent.parent.download_file(filename, new_dir)
            # send message to server
            #####mes2send = protocol.to_download_file(str(filename), new_dir)
            #####self.parent.parent.ccom.proc_send_message(mes2send)
        dlg.Destroy()
