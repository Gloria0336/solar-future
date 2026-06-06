"""
File-based help entries. These complements command-based help and help entries
added in the database using the `sethelp` command in-game.

Control where Evennia reads these entries with `settings.FILE_HELP_ENTRY_MODULES`,
which is a list of python-paths to modules to read.

A module like this should hold a global `HELP_ENTRY_DICTS` list, containing
dicts that each represent a help entry. If no `HELP_ENTRY_DICTS` variable is
given, all top-level variables that are dicts in the module are read as help
entries.

Each dict is on the form
::

    {'key': <str>,
     'text': <str>}``     # the actual help text. Can contain # subtopic sections
     'category': <str>,   # optional, otherwise settings.DEFAULT_HELP_CATEGORY
     'aliases': <list>,   # optional
     'locks': <str>       # optional, 'view' controls seeing in help index, 'read'
                          #           if the entry can be read. If 'view' is unset,
                          #           'read' is used for the index. If unset, everyone
                          #           can read/view the entry.

"""

HELP_ENTRY_DICTS = [
    {
        "key": "基本指令",
        "aliases": ["新手", "操作", "commands", "basic"],
        "category": "一般",
        "text": """
            # 基本操作

            你可以用中文或英文指令遊玩。常用指令如下：

            |w看|n / |wlook|n
                查看目前所在位置。

            |w看 <目標>|n / |wlook <target>|n
                查看附近的人、物品或出口。

            |w說 <訊息>|n / |wsay <message>|n
                對同一地點的人說話。

            |w密語 <角色> = <訊息>|n / |wwhisper <character> = <message>|n
                對指定角色悄悄說話。

            |w拿 <物品>|n / |wget <object>|n
                從所在地撿起物品。

            |w放下 <物品>|n / |wdrop <object>|n
                把身上的物品放到目前位置。

            |w給 <物品> = <角色>|n / |wgive <object> = <target>|n
                把身上的物品交給別人。

            |w背包|n / |winventory|n
                查看身上攜帶的物品。

            |w描述 <文字>|n / |wsetdesc <text>|n
                設定自己的角色描述。

            |w幫助|n / |whelp|n
                顯示說明。

            |w離開|n / |wquit|n
                中斷目前連線。
        """,
    },
    {
        "key": "evennia",
        "aliases": ["ev"],
        "category": "一般",
        "locks": "read:perm(Developer)",
        "text": """
            Evennia 是以 Python 撰寫的 MU 遊戲伺服器與框架。更多資訊可見：
            https://www.evennia.com

            # 子主題

            ## 安裝

            安裝說明可在 https://www.evennia.com 找到。

            ## 社群

            如果需要協助或想和其他開發者交流，可以參考以下管道。

            ### Discussions 討論區

            https://github.com/evennia/evennia/discussions

            ### Discord

            https://discord.gg/AJJpcRUhtF

        """,
    },
]
