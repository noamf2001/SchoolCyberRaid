import wx
import os
import sys
import wx.lib.agw.gradientbutton as GB
import wx.lib.agw.genericmessagedialog as GMD
import wx.lib.scrolledpanel
from my_popup_menu import MyPopupMenu


def find_loc(pos):
    if pos % 4 == 0:
        return 4
    elif pos % 3 == 0:
        return 3
    elif pos % 2 == 0:
        return 2
    return 1


class FilePanel(wx.lib.scrolledpanel.ScrolledPanel):
    PIC_SIZE = 75

    def __init__(self, parent):
        """Constructor"""

        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, -1,
                                                    size=(parent.screenWidth, parent.screenHeight * 0.9),
                                                    pos=(0, parent.screenHeight * 0.11),
                                                    style=wx.SIMPLE_BORDER)
        self.parent = parent

        self.PIC_SIZE = self.parent.screenHeight

        self.SetupScrolling()
        self.SetBackgroundColour(wx.Colour(117, 194, 229, 255))
        self.Refresh()

        self.set_ending_bmp()

    def set_ending_bmp(self):
        self.word_bmp = wx.Bitmap(self.parent.currentDirectory + "\\word.jpg")
        self.word_bmp = self.parent.scale_bitmap(self.word_bmp, FilePanel.PIC_SIZE, FilePanel.PIC_SIZE)

        self.excel_bmp = wx.Bitmap(self.parent.currentDirectory + "\\excel.jpg")
        self.excel_bmp = self.parent.scale_bitmap(self.excel_bmp, FilePanel.PIC_SIZE, FilePanel.PIC_SIZE)

        self.doc_bmp = wx.Bitmap(self.parent.currentDirectory + "\\doc.jpg")
        self.doc_bmp = self.parent.scale_bitmap(self.doc_bmp, FilePanel.PIC_SIZE, FilePanel.PIC_SIZE)

        self.jpg_bmp = wx.Bitmap(self.parent.currentDirectory + "\\jpg.png")
        self.jpg_bmp = self.parent.scale_bitmap(self.jpg_bmp, FilePanel.PIC_SIZE, FilePanel.PIC_SIZE)

        self.pp_bmp = wx.Bitmap(self.parent.currentDirectory + "\\powerp.jpg")
        self.pp_bmp = self.parent.scale_bitmap(self.pp_bmp, FilePanel.PIC_SIZE, FilePanel.PIC_SIZE)

        self.python_bmp = wx.Bitmap(self.parent.currentDirectory + "\\python_logo.png")
        self.python_bmp = self.parent.scale_bitmap(self.python_bmp, FilePanel.PIC_SIZE, FilePanel.PIC_SIZE)

        self.mp3_bmp = wx.Bitmap(self.parent.currentDirectory + "\\mp3_logo.jpg")
        self.mp3_bmp = self.parent.scale_bitmap(self.mp3_bmp, FilePanel.PIC_SIZE, FilePanel.PIC_SIZE)

        self.qm_bmp = wx.Bitmap(self.parent.currentDirectory + "\\question_mark.jpg")
        self.qm_bmp = self.parent.scale_bitmap(self.qm_bmp, FilePanel.PIC_SIZE, FilePanel.PIC_SIZE)



    def show_files(self, search=None):
        print "start"
        self.DestroyChildren()
        bSizer = wx.BoxSizer(wx.HORIZONTAL)
        dSizer = wx.BoxSizer(wx.VERTICAL)

        if search:
            file_show = [x for x in self.parent.files if search in x]
        else:
            file_show = self.parent.files
        print "files show: " + str(file_show)
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD)
        ind = 0
        counter = 0
        for file_name in file_show:
            try:
                ending = file_name[file_name.index('.'):].lower()
            except:
                continue

            cSizer = wx.BoxSizer(wx.VERTICAL)
            Xp = 75 * (counter + 1) + FilePanel.PIC_SIZE * counter
            counter += 1
            Yp = find_loc(counter) * 50

            if ending == ".docx" or ending == ".doc":
                button_file = wx.BitmapButton(self, -1, self.word_bmp, pos=(Xp, Yp))
            elif ending == ".xlsx" or ending == ".xls" or ending == ".pub":
                button_file = wx.BitmapButton(self, -1, self.excel_bmp, pos=(Xp, Yp))
            elif ending == ".jpg" or ending == ".png":
                button_file = wx.BitmapButton(self, -1, self.jpg_bmp, pos=(Xp, Yp))
            elif ending == ".pptx" or ending == ".ppt":
                button_file = wx.BitmapButton(self, -1, self.pp_bmp, pos=(Xp, Yp))
            elif ending == ".txt":
                button_file = wx.BitmapButton(self, -1, self.doc_bmp, pos=(Xp, Yp))
            elif ending == ".py" or ending == ".pyc":
                button_file = wx.BitmapButton(self, -1, self.python_bmp, pos=(Xp, Yp))
            elif ending == ".mp3":
                button_file = wx.BitmapButton(self, -1, self.mp3_bmp, pos=(Xp, Yp))
            else:
                button_file = wx.BitmapButton(self, -1, self.mp3_bmp, pos=(Xp, Yp))

            button_file.SetLabel(file_name)
            button_file.Bind(wx.EVT_BUTTON, self.OnButton_Press)

            if len(file_name) > 11:
                text = wx.StaticText(self, -1, pos=(self.parent.screenWidth * 0.039, self.parent.screenHeight * 0.12),
                                     size=(self.parent.screenWidth * 0.059, self.parent.screenHeight * 0.036),
                                     label=file_name[:7] + ".." + file_name[file_name.find("."):])
            else:
                text = wx.StaticText(self, -1, pos=(self.parent.screenWidth * 0.039, self.parent.screenHeight * 0.12),
                                     size=(self.parent.screenWidth * 0.059, self.parent.screenHeight * 0.036),
                                     label=file_name)
            text.SetFont(font)

            cSizer.Add(button_file, 0, wx.ALL, 10)
            cSizer.Add(text, 0, wx.CENTER, 5)
            bSizer.Add(cSizer, 0, wx.CENTER, 25)
            ind += 1

            if ind == 8:
                dSizer.Add(bSizer, 0, wx.CENTER, 15)
                ind = 0
                counter = 0
                bSizer = wx.BoxSizer(wx.HORIZONTAL)

        if ind != 0:
            dSizer.Add(bSizer, 0, wx.CENTER, 5)

        self.SetSizer(dSizer)

        self.Layout()
        self.SetupScrolling()

    def OnButton_Press(self, event):
        btn = event.GetEventObject()
        pos = btn.GetPosition()
        menu = MyPopupMenu(btn.GetLabelText(), self)
        self.PopupMenu(menu, (btn.GetPosition()[0] + 80, btn.GetPosition()[1] + 60))
        menu.Destroy()
