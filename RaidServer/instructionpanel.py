import wx
INSTRUCTION_TEXT = "bleblable\nbery boring dfghjkjhgfdsdfhjkl\nkjhgfdchjkkhfcxgjkllg\next"

class InstructionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        wx.StaticText(
            self, -1, INSTRUCTION_TEXT, (0, 0), (120, -1), wx.ALIGN_CENTER
            ).SetBackgroundColour('Yellow')