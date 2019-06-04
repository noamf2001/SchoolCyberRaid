import wx

INSTRUCTION_TEXT = "this is the server GUI for admin\n" \
    "data server - the data server that are connected to the server - you can press and find all the parts that is saved on them\n"\
                   "file: all the files that the server saved - you can click and see who it belongs to\n" \
                   "data servers settings: all the data server in the local network - that can connect to the server - you can add or remove\n"


class InstructionPanel(wx.Panel):
    def __init__(self, parent, screenWidth, screenHeight):
        """
        constructor of instruction panel
        :param parent:
        :param screenWidth:
        :param screenHeight:
        """
        wx.Panel.__init__(self,  parent)
        self.SetBackgroundColour(wx.Colour(117, 194, 229, 255))
        wx.StaticText(
            self, -1, INSTRUCTION_TEXT, (0, 0), size=(screenWidth, screenHeight * 0.9), style = wx.ALIGN_CENTER
        ).SetBackgroundColour('Yellow')
        about_img = wx.Image(
            "about.png",
            wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        about = wx.StaticBitmap(
            self, -1, about_img, (screenWidth/3, screenHeight/3), size = (screenWidth/3, screenHeight/3))
        wx.StaticText(
            self, -1, "Made by: Noam Fluss", ( screenWidth/2 - 50, 3*screenHeight/4)
        )