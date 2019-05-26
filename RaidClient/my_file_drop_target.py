import wx


class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        """
        constructor
        :param window: the window which is allowed to drop on
        """
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        """
        When files are dropped, write where they were dropped and then
        the file paths themselves
        """
        self.window.parent.upload_files(filenames)
