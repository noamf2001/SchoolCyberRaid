import wx
INSTRUCTION_TEXT = "this is the server GUI for admin\n"
                   #"files page: all the files that the server saved - you can click and see who it belongs to\n" \
                   #"data servers settings: all the data server in the local network - that can connect to the server - you can add or remove\n" \
                   #"data server - the data server that are connected to the server - you can press and find all the parts that is saved on them"

class InstructionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        wx.StaticText(
            self, -1, INSTRUCTION_TEXT, (0, 0), (120, -1), wx.ALIGN_CENTER
            ).SetBackgroundColour('Yellow')