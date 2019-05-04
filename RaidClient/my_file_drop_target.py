import wx


class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        """
        When files are dropped, write where they were dropped and then
        the file paths themselves
        """
        print "drop files: " + str(filenames)
        self.window.parent.upload_files(filenames)
        ####msg2send = protocol.to_upload_file(str(filename))
        ####self.window.parent.ccom.proc_send_message(msg2send)
