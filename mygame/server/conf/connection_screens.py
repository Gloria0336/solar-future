# -*- coding: utf-8 -*-
"""
Connection screen

This is the text to show the user when they first connect to the game (before
they log in).

To change the login screen in this module, do one of the following:

- Define a function `connection_screen()`, taking no arguments. This will be
  called first and must return the full string to act as the connection screen.
  This can be used to produce more dynamic screens.
- Alternatively, define a string variable in the outermost scope of this module
  with the connection string that should be displayed. If more than one such
  variable is given, Evennia will pick one of them at random.

The commands available to the user when the connection screen is shown
are defined in evennia.default_cmds.UnloggedinCmdSet. The parsing and display
of the screen is done by the unlogged-in "look" command.

"""

from django.conf import settings

from evennia import utils

CONNECTION_SCREEN = """
|b==============================================================|n
 歡迎來到 |g{}|n，版本 {}！

 已有帳號：
      |w登入 <帳號> <密碼>|n
      |wconnect <username> <password>|n

 建立新帳號：
      |w註冊 <帳號> <密碼>|n
      |wcreate <username> <password>|n

 如果帳號或密碼含有空白，請用雙引號包起來。
 輸入 |w幫助|n 查看說明；輸入 |w看|n 重新顯示此畫面。
|b==============================================================|n""".format(
    settings.SERVERNAME, utils.get_evennia_version("short")
)
