import wx
import os
import sys
import wx.lib.agw.gradientbutton as GB
import wx.lib.agw.genericmessagedialog as GMD
import wx.lib.scrolledpanel


def find_loc(pos):
    if pos % 4 == 0:
        return 4
    elif pos % 3 == 0:
        return 3
    elif pos % 2 == 0:
        return 2
    return 1


class FilesPanel(wx.lib.scrolledpanel.ScrolledPanel):

    def __init__(self, parent, set_ending_bmp, get_icon, screenWidth, screenHeight, is_data_server, OnButton_Press,
                 files, pos_h=0, right_click_press=None):
        self.files = files
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        if pos_h == 0:
            pos_h = self.screenHeight * 0.11
        self.is_data_server = is_data_server
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, -1,
                                                    size=(self.screenWidth, self.screenHeight * 0.9),
                                                    pos=(0, pos_h),
                                                    style=wx.SIMPLE_BORDER)
        self.PIC_SIZE = self.screenWidth / 9.5
        self.SetupScrolling()
        self.SetBackgroundColour(wx.Colour(117, 194, 229, 255))
        self.Refresh()
        set_ending_bmp()
        self.get_icon = get_icon

        self.OnButton_Press = OnButton_Press
        self.right_click_press = right_click_press
        self.Bind(wx.EVT_CONTEXT_MENU, self.right_click_press)


    def show_files(self, search=None):
        self.DestroyChildren()
        bSizer = wx.BoxSizer(wx.HORIZONTAL)
        dSizer = wx.BoxSizer(wx.VERTICAL)
        if search:
            file_show = [x for x in self.files if search in x]
        else:
            file_show = self.files
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD)
        small_font = wx.Font(9, wx.MODERN, wx.NORMAL, wx.BOLD)
        ind = 0
        for file_name in file_show:
            if not self.is_data_server:
                ending = file_name[file_name.index('.'):].lower()
            else:
                ending = ""
            cSizer = wx.BoxSizer(wx.VERTICAL)
            button_file = wx.BitmapButton(self, -1, self.get_icon(ending))

            button_file.SetLabel(file_name)
            button_file.Bind(wx.EVT_BUTTON, self.OnButton_Press)
            if len(file_name) > 13:
                if self.is_data_server:
                    text = wx.StaticText(self, -1,
                                         size=(self.PIC_SIZE, 20),
                                         label=file_name)
                    text.SetFont(small_font)
                else:
                    text = wx.StaticText(self, -1,
                                         size=(self.PIC_SIZE, 20),
                                         label=file_name[:11 - len(ending)] + ".." + ending)
                    text.SetFont(font)
            else:
                text = wx.StaticText(self, -1,
                                     size=(self.PIC_SIZE, 20),
                                     label=file_name)
                text.SetFont(font)

            cSizer.Add(button_file, 0, wx.ALL, self.PIC_SIZE / 9)
            cSizer.Add(text, 0, wx.CENTER, 10)
            bSizer.Add(cSizer, 0, wx.CENTER, 0)
            ind += 1

            if ind == 7:
                dSizer.Add(bSizer, 0, wx.CENTER, 0)
                ind = 0
                bSizer = wx.BoxSizer(wx.HORIZONTAL)

        if ind != 0:
            dSizer.Add(bSizer, 0, wx.CENTER, 5)

        self.SetSizer(dSizer)

        self.Layout()
        self.SetupScrolling()
