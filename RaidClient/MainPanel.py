import wx
import os
import sys
from SignDialog import SignDialog
import wx.lib.agw.gradientbutton as GB
import wx.lib.agw.genericmessagedialog as GMD
import wx.lib.scrolledpanel
from search_control import SearchControl
import wx.lib.dialogs

INSTRUCTION = "this is the instruction for Raid:\nblablabla\nthis is thhe end"


class MainPanel(wx.Panel):
    WILDCARD = "Python source (*.py)|*.py|" \
               "Compiled Python (*.pyc)|*.pyc|" \
               "SPAM files (*.spam)|*.spam|" \
               "Egg file (*.egg)|*.egg|" \
               "All files (*.*)|*.*"

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(parent.screenWidth, parent.screenHeight * 0.1),
                          pos=(0, 0),
                          style=wx.SIMPLE_BORDER)
        wx.Colour(117, 194, 229, 255)

        self.SetBackgroundColour(wx.Colour(117, 194, 229, 255))
        self.parent = parent
        # sizer2 = wx.BoxSizer( wx.HORIZONTAL )

        sc = SearchControl(self.parent, self, -1, "", size=(self.parent.screenWidth * 0.1, parent.screenHeight * 0.06),
                           pos=(self.parent.screenWidth * 0.86, parent.screenHeight * 0.02))
        self.show_message(msg="My Files:", pos=(self.parent.screenWidth * 0.02, self.parent.screenHeight * 0.027))

        upload_file_button = wx.Button(self, -1, "upload file",
                                       size=(self.parent.screenWidth * 0.1, self.parent.screenHeight * 0.06),
                                       pos=(self.parent.screenWidth * 0.15, self.parent.screenHeight * 0.02))
        self.Bind(wx.EVT_BUTTON, self.on_button_upload_file, upload_file_button)

        instruction_button = wx.Button(self, -1, "Instructions",
                                       size=(self.parent.screenWidth * 0.1, self.parent.screenHeight * 0.06),
                                       pos=(self.parent.screenWidth * 0.27, self.parent.screenHeight * 0.02))
        self.Bind(wx.EVT_BUTTON, self.on_button_instruction, instruction_button)

        self.show_message(msg="-Drag   Files   Below-",
                          pos=(self.parent.screenWidth * 0.45, self.parent.screenHeight * 0.027))


    def on_button_instruction(self, evt):
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, INSTRUCTION,
                                                   'Raid instructions')
        dlg.ShowModal()
        dlg.Destroy()


    def on_button_upload_file(self, evt):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=MainPanel.WILDCARD,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()

            self.parent.upload_files(paths)
        dlg.Destroy()


    def show_message(self, msg, pos):
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        msg = wx.StaticText(self, label=msg, pos=pos)
        msg.SetForegroundColour(wx.BLACK)
        msg.SetFont(font)
