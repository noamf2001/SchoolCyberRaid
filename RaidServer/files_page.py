from files_panel import FilesPanel
import wx
import wx.lib.dialogs

class FilesPage():
    def __init__(self, parent, nb, files, users_files):
        self.parent = parent
        self.users_files = users_files
        self.files = files
        self.PIC_SIZE = self.parent.screenWidth / 9.5
        self.files_panel = FilesPanel(nb, self.set_ending_bmp, self.get_icon,
                                      self.parent.screenWidth, self.parent.screenHeight, False, self.OnButton_Press,self.files)
        self.files_panel.show_files()



    def set_ending_bmp(self):
        self.word_bmp = wx.Bitmap(self.parent.currentDirectory + "\\word.jpg")
        self.word_bmp = self.parent.scale_bitmap(self.word_bmp, self.PIC_SIZE, self.PIC_SIZE)

        self.excel_bmp = wx.Bitmap(self.parent.currentDirectory + "\\excel.jpg")
        self.excel_bmp = self.parent.scale_bitmap(self.excel_bmp, self.PIC_SIZE, self.PIC_SIZE)

        self.doc_bmp = wx.Bitmap(self.parent.currentDirectory + "\\doc.jpg")
        self.doc_bmp = self.parent.scale_bitmap(self.doc_bmp, self.PIC_SIZE, self.PIC_SIZE)

        self.jpg_bmp = wx.Bitmap(self.parent.currentDirectory + "\\jpg.png")
        self.jpg_bmp = self.parent.scale_bitmap(self.jpg_bmp, self.PIC_SIZE, self.PIC_SIZE)

        self.pp_bmp = wx.Bitmap(self.parent.currentDirectory + "\\powerp.jpg")
        self.pp_bmp = self.parent.scale_bitmap(self.pp_bmp, self.PIC_SIZE, self.PIC_SIZE)

        self.python_bmp = wx.Bitmap(self.parent.currentDirectory + "\\python_logo.png")
        self.python_bmp = self.parent.scale_bitmap(self.python_bmp, self.PIC_SIZE, self.PIC_SIZE)

        self.mp3_bmp = wx.Bitmap(self.parent.currentDirectory + "\\mp3_logo.jpg")
        self.mp3_bmp = self.parent.scale_bitmap(self.mp3_bmp, self.PIC_SIZE, self.PIC_SIZE)

        self.qm_bmp = wx.Bitmap(self.parent.currentDirectory + "\\question_mark.jpg")
        self.qm_bmp = self.parent.scale_bitmap(self.qm_bmp, self.PIC_SIZE, self.PIC_SIZE)

    def get_icon(self, ending):
        if ending == ".docx" or ending == ".doc":
            return self.word_bmp
        elif ending == ".xlsx" or ending == ".xls" or ending == ".pub":
            return self.excel_bmp
        elif ending == ".jpg" or ending == ".png":
            return self.jpg_bmp
        elif ending == ".pptx" or ending == ".ppt":
            return self.pp_bmp
        elif ending == ".txt":
            return self.doc_bmp
        elif ending == ".py" or ending == ".pyc":
            return self.python_bmp
        elif ending == ".mp3":
            return self.mp3_bmp
        else:
            return self.qm_bmp

    def OnButton_Press(self, event):
        print "press files"
        btn = event.GetEventObject()
        file_name = btn.GetLabelText()
        dlg = wx.MessageDialog(self.files_panel, "the user that have this file is: " + self.users_files[file_name], "file: " + file_name,wx.OK | wx.ICON_INFORMATION
                                                   )
        dlg.ShowModal()
        dlg.Destroy()
