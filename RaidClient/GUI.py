import wx
import wx.lib.scrolledpanel
import sys
import wx.lib.agw.gradientbutton as GB
import os
import wx.lib.agw.genericmessagedialog as GMD
import pickle
import uuid
import wx.lib.pubsub.setupkwargs
from wx.lib.pubsub import pub

class GUI(wx.Frame):
    def __init__(self):
