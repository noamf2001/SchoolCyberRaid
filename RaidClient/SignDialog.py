import wx
import sys


class SignDialog(wx.Dialog):
    """
    Class to define login dialog
    """

    def __init__(self, parent):
        """Constructor"""
        screenSize = wx.DisplaySize()
        self.screenWidth = screenSize[0] * 0.6
        self.screenHeight = (screenSize[1]) * 0.6

        self.client = parent.client
        wx.Dialog.__init__(self, parent, title="Network Raid", size=(self.screenWidth, self.screenHeight),
                           pos=(0, 0))
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.Bind(wx.EVT_CLOSE, self._when_closed)
        self.parent = parent

        BackgroundBmp = wx.Bitmap("raidIcon.jpg")
        image = wx.ImageFromBitmap(BackgroundBmp)
        image = image.Scale(self.screenWidth * 0.5, self.screenHeight * 0.4, wx.IMAGE_QUALITY_HIGH)
        BackgroundBmp = wx.BitmapFromImage(image)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        text_ctrl_parameters_sizer = wx.BoxSizer(wx.VERTICAL)

        sBitMap = wx.StaticBitmap(self, -1, BackgroundBmp, (10, 10),
                                  (BackgroundBmp.GetWidth(), BackgroundBmp.GetHeight()))
        sign_button_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(sBitMap, 0, wx.ALL | wx.CENTER, 5)

        self.username_ctrl = wx.TextCtrl(self, size=(self.screenWidth * 150 / 1051, self.screenHeight * 9 / 192))
        self.username_ctrl.SetHint("username")

        text_ctrl_parameters_sizer.Add(self.username_ctrl, 0, wx.ALL | wx.CENTER, 5)

        self.password_ctrl = wx.TextCtrl(self, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER,
                                         size=(self.screenWidth * 150 / 1051, self.screenHeight * 9 / 192))
        self.password_ctrl.SetHint("password")

        text_ctrl_parameters_sizer.Add(self.password_ctrl, 0, wx.ALL | wx.CENTER, 5)

        btn2 = wx.Button(self, label="Sign In", size=(self.screenWidth * 150 / 1051, self.screenHeight * 9 / 192))
        btn2.Bind(wx.EVT_BUTTON, self.onSignIn)
        sign_button_sizer.Add(btn2, 0, wx.ALL | wx.CENTER, 5)

        btn1 = wx.Button(self, label="Sign Up", size=(self.screenWidth * 150 / 1051, self.screenHeight * 9 / 192))
        btn1.Bind(wx.EVT_BUTTON, self.onSignUp)

        sign_button_sizer.Add(btn1, 0, wx.ALL | wx.CENTER, 5)

        main_sizer1 = wx.BoxSizer(wx.HORIZONTAL)

        main_sizer1.Add(text_ctrl_parameters_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer1.Add(sign_button_sizer, 0, wx.ALL | wx.CENTER, 5)

        main_sizer.Add(main_sizer1, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(main_sizer)
        self.sign_result = ""

    def onSignIn(self, event):
        """
        Check credentials and login
        """
        password = self.password_ctrl.GetValue()
        username = self.username_ctrl.GetValue()
        self.client.sign_in(username, password)

    def onSignUp(self, event):
        """
        Check credentials and login
        """
        password = self.password_ctrl.GetValue()
        username = self.username_ctrl.GetValue()
        if not self.client.check_legal_username(username):
            self.show_message("username is not legal", (100, 200))
        elif not self.client.check_legal_password(password):
            self.show_message("password is not legal", (100, 200))
        self.client.sign_up(username, password)

    def show_message(self, message, pos):
        """
        show message to user after finish press
        :param message: the message to show the user - the result of the try to sign
        :param pos
        """
        if self.sign_result != "":
            self.sign_result.Destroy()
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.sign_result = wx.StaticText(self, label=message, pos=pos)
        self.sign_result.SetForegroundColour(wx.BLACK)
        self.sign_result.SetFont(font)

    def _when_closed(self, event):
        sys.exit()
