import wx
import os
import sys
from SignDialog import SignDialog
import wx.lib.agw.gradientbutton as GB
import wx.lib.agw.genericmessagedialog as GMD
import wx.lib.scrolledpanel
from search_control import SearchControl


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(parent.screenWidth * 0.82, parent.screenHeight * 0.06),
                          pos=(parent.screenWidth * 0.179 - 4, 0),
                          style=wx.SIMPLE_BORDER)
        wx.Colour(117, 194, 229, 255)

        self.SetBackgroundColour(wx.Colour(117, 194, 229, 255))
        self.parent = parent
        # sizer2 = wx.BoxSizer( wx.HORIZONTAL )

        sc = SearchControl(self.parent, self, -1, "", (self.parent.screenWidth * 0.69, 0))
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.show_message(message="My Files:", pos=(self.parent.screenWidth * 0.013, self.parent.screenWidth * 0.012))
        '''
        quote = wx.StaticText(self, label="My Files:",pos=(self.parent.screenWidth*0.013,self.parent.screenWidth*0.012))
        quote.SetFont(font)
        '''
        # sizer2.Add(quote)



    def show_message(self, message=None, pos=None):
        try:
            self.username_msg.Destroy()
        except:
            pass
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        if message:
            self.username_msg = wx.StaticText(self, label=message, pos=pos)
            self.username_msg.SetForegroundColour(wx.BLACK)
            self.username_msg.SetFont(font)

        else:
            try:
                self.username_msg.Destroy()
            except:
                pass
