import wx


class SearchControl(wx.SearchCtrl):
    def __init__(self, grandfather, parent, id, value='', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TE_PROCESS_ENTER):
        wx.SearchCtrl.__init__(self, parent, id, value, pos, size, style)
        self.grandfather = grandfather
        self.parent = parent
        self.SetFocus()
        self.Bind(wx.EVT_TEXT_ENTER, self.SearchHandler)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.SearchHandler)
        self.Show()

    def SearchHandler(self, event):
        self.parent.parent.file_panel.show_files(event.GetString())
