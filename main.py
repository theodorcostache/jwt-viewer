#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
import sys
import json
import base64

class JWTDecoderFrame(wx.Frame):

    def __init__(self, parent, title):
        super(JWTDecoderFrame, self).__init__(parent, title=title, size=(800, 600))

        self.panel = wx.Panel(self)
        self.statusbar = self.CreateStatusBar(1)

        self.token_input = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE, size=(-1,100))
        self.token_input.Bind(wx.EVT_KEY_UP, self.handle_token_input)

        self.splitter = wx.SplitterWindow(self.panel)
        self.header_panel = wx.Panel(self.splitter)
        self.payload_panel = wx.Panel(self.splitter)

        self.header_output = wx.TextCtrl(self.header_panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.payload_output = wx.TextCtrl(self.payload_panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.layout_ui()
        self.Centre()

    def layout_input(self, panel, token_input, font):

        vBox = wx.BoxSizer(wx.VERTICAL)

        st1 = wx.StaticText(panel, label='Token:')
        st1.SetFont(font)
        vBox.Add(st1)
        vBox.Add(token_input, proportion=1, flag=wx.EXPAND)
        
        return vBox

    def layout_decode_section(self, panel, output_area, font, label):

        vbox = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(panel, label=label)
        st.SetFont(font)
        vbox.Add(st , 0)
        vbox.Add((-1, 10))
        vbox.Add(output_area, 1, flag=wx.EXPAND)

        return vbox

    def layout_ui(self):

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.layout_input(self.panel, self.token_input, font), 0, flag=wx.EXPAND | wx.ALL, border=5)

        self.header_panel.SetSizer(self.layout_decode_section(self.header_panel, self.header_output, font, 'Header:'))
        self.payload_panel.SetSizer(self.layout_decode_section(self.payload_panel, self.payload_output, font, 'Payload:'))

        self.splitter.SplitVertically(self.header_panel, self.payload_panel, 400)    

        vbox.Add((-1, 10))
        vbox.Add(self.splitter, 1, flag=wx.EXPAND | wx.ALL, border=5)

        self.panel.SetSizer(vbox)
        self.panel.Layout()

    def handle_token_input(self, Evt):

        token = self.token_input.GetValue()
        parts = token.strip().split(".")
        headerJson = ""
        payloadJson = ""
        header = {}
        payload = {}

        if token != "":
            try:
                header_str = base64.b64decode(parts[0] + "=" * ((4 - len(parts[0])) % 4))
                header = json.loads(header_str)
                headerJson = json.dumps(header, sort_keys=True, indent=4)
                self.header_output.ChangeValue(headerJson)
            except:
                print(sys.exc_info())
                self.header_output.ChangeValue(f"{sys.exc_info()[0]}")

            try: 
                payload_str = base64.b64decode(parts[1] + "=" * ((4 - len(parts[1])) % 4))
                payload = json.loads(payload_str)
                payloadJson = json.dumps(payload, sort_keys=True, indent=4)
                self.payload_output.ChangeValue(payloadJson)
            except:
                print(sys.exc_info())
                self.payload_output.ChangeValue(f"{sys.exc_info()[0]}")


def main():

    app = wx.App()
    ex = JWTDecoderFrame(None, title='JWT Decoder')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
