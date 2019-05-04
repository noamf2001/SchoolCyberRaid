from my_file_drop_target import MyFileDropTarget
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
    """"""

    def __init__(self, parent):
        """Constructor"""

        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, -1,
                                                    size=(parent.screenWidth * 0.82, parent.screenHeight * 0.95),
                                                    pos=(parent.screenWidth * 0.179, parent.screenHeight * 0.06),
                                                    style=wx.SIMPLE_BORDER)
        self.parent = parent
        self.filelst = parent.init_files
        ######################
        self.SetupScrolling()
        self.SetBackgroundColour(wx.Colour(117, 194, 229, 255))
        self.Refresh()
        ###################
        self.show_message(message="-Drag   Files   Here-", pos=(
            self.parent.screenWidth * 0.179 + self.parent.screenWidth * 0.82 / 5,
            self.parent.screenHeight * 0.06 + self.parent.screenHeight * 0.95 / 3), color=wx.WHITE)

        # self.show_message("-Drag Files Here-",pos=(parent.screenWidth*0.179+parent.screenWidth*0.82/2,parent.screenHeight*0.06+parent.screenHeight*0.95/2))
        dt = MyFileDropTarget(self)
        self.SetDropTarget(dt)

        if self.filelst:
            self.draw_homescreen_files()

    def show_message(self, message=None, pos=None, color=None):
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        if message:
            self.username_msg = wx.StaticText(self, label=message, pos=pos)
            self.username_msg.SetFont(font)
            if color:
                self.username_msg.SetForegroundColour(color)
            else:
                self.username_msg.SetForegroundColour(wx.BLACK)

        else:
            try:
                self.username_msg.Destroy()
            except:
                pass

    def draw_homescreen_files(self, init_files=None, search=None):
        # enter:receives a file name
        # exit: shows file in home screen with its name and file type
        if init_files:
            self.filelst = init_files
            self.parent.init_files = init_files

        bSizer = wx.BoxSizer(wx.HORIZONTAL)
        dSizer = wx.BoxSizer(wx.VERTICAL)

        if search:
            filelst = [x for x in self.filelst if search in x[:x.find(".")]]
        else:
            filelst = self.filelst

        if not filelst:
            # file not found
            filelst = self.filelst
            self.show_message(search)
        else:
            self.show_message()

        '''
        if not filelst:
            #file not found
            #self.show_message("the file doesn't exist",pos=(400,400))
            filelst = self.filelst
            if len(search) > 15:
                search = search[0:7]+"..."+search[-4:]
            return
        else:
            self.show_message()
        '''
        picSize = 75
        WordBmp = wx.Bitmap(self.parent.currentDirectory + "\\word.jpg")
        WordBmp = self.parent.scale_bitmap(WordBmp, picSize, picSize)
        ExcelBmp = wx.Bitmap(self.parent.currentDirectory + "\\excel.jpg")
        ExcelBmp = self.parent.scale_bitmap(ExcelBmp, picSize, picSize)
        DocBmp = wx.Bitmap(self.parent.currentDirectory + "\\doc.jpg")
        DocBmp = self.parent.scale_bitmap(DocBmp, picSize, picSize)
        JpgBmp = wx.Bitmap(self.parent.currentDirectory + "\\jpg.png")
        JpgBmp = self.parent.scale_bitmap(JpgBmp, picSize, picSize)
        PPBmp = wx.Bitmap(self.parent.currentDirectory + "\\powerp.jpg")
        PPBmp = self.parent.scale_bitmap(PPBmp, picSize, picSize)
        TXTBmp = wx.Bitmap(self.parent.currentDirectory + "\\txt_logo.png")
        TXTBmp = self.parent.scale_bitmap(TXTBmp, picSize, picSize)
        PythonBmp = wx.Bitmap(self.parent.currentDirectory + "\\python_logo.png")
        PythonBmp = self.parent.scale_bitmap(PythonBmp, picSize, picSize)
        mp3Bmp = wx.Bitmap(self.parent.currentDirectory + "\\mp3_logo.png")
        mp3Bmp = self.parent.scale_bitmap(mp3Bmp, picSize, picSize)

        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD)
        ind = 0
        counter = 0
        types_list = [".py", ".pyc", ".docx", ".doc", ".xlsx", ".xls", ".pub", ".jpg", ".png", ".pptx", ".ppt", ".txt",
                      ".mp3"]
        for itm in filelst:
            print itm
            try:
                ending = itm[itm.index('.'):].lower()
            except:
                continue

            if ending not in types_list:
                continue
            cSizer = wx.BoxSizer(wx.VERTICAL)
            Xp = 75 * (counter + 1) + picSize * counter
            counter += 1
            Yp = find_loc(counter) * 50

            if ending == ".docx" or ending == ".doc":
                button1 = wx.BitmapButton(self, -1, WordBmp, pos=(Xp, Yp))
            elif ending == ".xlsx" or ending == ".xls" or ending == ".pub":
                button1 = wx.BitmapButton(self, -1, ExcelBmp, pos=(Xp, Yp))

            elif ending == ".jpg" or ending == ".png":
                button1 = wx.BitmapButton(self, -1, JpgBmp, pos=(Xp, Yp))
            elif ending == ".pptx" or ending == ".ppt":
                button1 = wx.BitmapButton(self, -1, PPBmp, pos=(Xp, Yp))
            elif ending == ".txt":
                button1 = wx.BitmapButton(self, -1, TXTBmp, pos=(Xp, Yp))
            elif ending == ".py" or ending == ".pyc":
                button1 = wx.BitmapButton(self, -1, PythonBmp, pos=(Xp, Yp))
            elif ending == ".mp3":
                button1 = wx.BitmapButton(self, -1, mp3Bmp, pos=(Xp, Yp))

            button1.SetLabel(itm)
            button1.Bind(wx.EVT_BUTTON, self.OnButton_Press)

            if len(itm) > 11:
                text = wx.StaticText(self, -1, pos=(self.parent.screenWidth * 0.039, self.parent.screenHeight * 0.12),
                                     size=(self.parent.screenWidth * 0.059, self.parent.screenHeight * 0.036),
                                     label=itm[:7] + ".." + itm[itm.find("."):])
            else:
                text = wx.StaticText(self, -1, pos=(self.parent.screenWidth * 0.039, self.parent.screenHeight * 0.12),
                                     size=(self.parent.screenWidth * 0.059, self.parent.screenHeight * 0.036),
                                     label=itm)
            text.SetFont(font)

            cSizer.Add(button1, 0, wx.ALL, 10)
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
        self.show_message(message="-Drag   Files   Here-", pos=(
            self.parent.screenWidth * 0.179 + self.parent.screenWidth * 0.82 / 5,
            self.parent.screenHeight * 0.06 + self.parent.screenHeight * 0.95 / 3), color=wx.WHITE)

    def onSaveFile(self, event):
        """
        Create and show the Save FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Save file as ...",
            defaultDir=self.parent.currentDirectory,
            defaultFile="", style=wx.FD_SAVE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            # print "You chose the following filename: %s" % path
        dlg.Destroy()

    def OnButton_Press(self, event):
        btn = event.GetEventObject()
        pos = btn.GetPosition()
        menu = MyPopupMenu(btn.GetLabelText(), self)
        self.PopupMenu(menu, (btn.GetPosition()[0] + 80, btn.GetPosition()[1] + 60))
        menu.Destroy()
