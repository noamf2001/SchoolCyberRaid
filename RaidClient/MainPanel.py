import wx
import os
import sys
from SignDialog import SignDialog
import wx.lib.agw.gradientbutton as GB
import wx.lib.agw.genericmessagedialog as GMD
import wx.lib.scrolledpanel
from search_control import SearchControl
import wx.lib.dialogs

INSTRUCTION = "This is the instruction for Network Raid:\n" \
              "to save files please drop them on the screen or choose using the upload button\n" \
              "to download/delete a file, press it, and choose the action\n\n\n\n" \
              "made by Noam Fluss"


class MainPanel(wx.Panel):
    WILDCARD = "Python source (*.py)|*.py|" \
               "Compiled Python (*.pyc)|*.pyc|" \
               "SPAM files (*.spam)|*.spam|" \
               "Egg file (*.egg)|*.egg|" \
               "All files (*.*)|*.*"

    def __init__(self, parent):
        """
        constructor
        :param parent: for init
        """
        wx.Panel.__init__(self, parent, size=(parent.screenWidth, parent.screenHeight * 0.1),
                          pos=(0, 0),
                          style=wx.SIMPLE_BORDER)
        wx.Colour(117, 194, 229, 255)

        self.SetBackgroundColour(wx.Colour(117, 194, 229, 255))
        self.parent = parent
        # create search box
        sc = SearchControl(self.parent, self, -1, "", size=(self.parent.screenWidth * 0.1, parent.screenHeight * 0.06),
                           pos=(self.parent.screenWidth * 0.86, parent.screenHeight * 0.02))
        self.show_message(msg="My Files:", pos=(self.parent.screenWidth * 0.02, self.parent.screenHeight * 0.027))
        # create upload button
        upload_file_button = wx.Button(self, -1, "upload file",
                                       size=(self.parent.screenWidth * 0.1, self.parent.screenHeight * 0.06),
                                       pos=(self.parent.screenWidth * 0.15, self.parent.screenHeight * 0.02))
        self.Bind(wx.EVT_BUTTON, self.on_button_upload_file, upload_file_button)
        # create instruction button
        instruction_button = wx.Button(self, -1, "Instructions",
                                       size=(self.parent.screenWidth * 0.1, self.parent.screenHeight * 0.06),
                                       pos=(self.parent.screenWidth * 0.27, self.parent.screenHeight * 0.02))
        self.Bind(wx.EVT_BUTTON, self.on_button_instruction, instruction_button)

        self.show_message(msg="-Drag   Files   Below-",
                          pos=(self.parent.screenWidth * 0.45, self.parent.screenHeight * 0.027))

    def on_button_instruction(self, evt):
        """
        the method called after pressing instruction button
        :param evt: the event that describe the press - do not need it
        """
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, INSTRUCTION,
                                                   'Raid instructions')
        dlg.ShowModal()
        dlg.Destroy()

    def on_button_upload_file(self, evt):
        """
        the method called after pressing upload button
        :param evt: the event that describe the press - do not need it
        """
        # choose file dialog
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
        """
        print a msg on the screen
        :param msg: a msg to show on panel
        :param pos: the pos to put it
        """
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        msg = wx.StaticText(self, label=msg, pos=pos)
        msg.SetForegroundColour(wx.BLACK)
        msg.SetFont(font)
