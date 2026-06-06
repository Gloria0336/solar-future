"""
Chinese-facing player commands.

These commands keep the English command keys available while adding Chinese
aliases and translating the most common player-visible responses.
"""

import evennia
import re
from django.conf import settings
from evennia.commands.default import account, general, help as help_cmds, unloggedin
from evennia.utils import class_from_module, utils


def _name(obj, looker=None):
    """Return a display name without English articles."""
    return obj.get_display_name(looker or obj)


def _counted_name(obj, count, looker=None):
    """Return a Chinese-friendly counted object name."""
    name = _name(obj, looker)
    return name if count == 1 else f"{count} 個 {name}"


class CmdLook(general.CmdLook):
    """
    查看目前位置或附近物件。

    用法:
      看
      看 <物件>
      look <object>
    """

    aliases = ["l", "ls", "看", "查看", "瞧", "觀察"]
    help_category = "一般"

    def func(self):
        caller = self.caller
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("你目前沒有可查看的位置。")
                return
        else:
            target = caller.search(
                self.args,
                nofound_string=f"找不到「{self.args}」。",
                multimatch_string=f"找到多個「{self.args}」，請指定其中一個：",
            )
            if not target:
                return

        desc = caller.at_look(target)
        self.msg(text=(desc, {"type": "look"}), options=None)


class CmdInventory(general.CmdInventory):
    """
    查看身上攜帶的物品。

    用法:
      背包
      inventory
    """

    aliases = ["inv", "i", "背包", "物品", "身上", "行囊"]
    help_category = "一般"

    def func(self):
        items = self.caller.contents
        if not items:
            string = "你身上沒有攜帶任何物品。"
        else:
            from evennia.utils.ansi import raw as raw_ansi

            table = self.styled_table(border="header")
            for key, desc, _ in utils.group_objects_by_key_and_desc(items, caller=self.caller):
                table.add_row(
                    f"|C{key}|n",
                    "{}|n".format(utils.crop(raw_ansi(desc or ""), width=50) or ""),
                )
            string = f"|w你攜帶著：|n\n{table}"
        self.msg(text=(string, {"type": "inventory"}))


class CmdGet(general.CmdGet):
    """
    撿起所在地的物品。

    用法:
      拿 <物品>
      get <object>
    """

    aliases = ["grab", "拿", "撿", "拾取", "取得"]
    help_category = "一般"

    def func(self):
        caller = self.caller

        if not self.args:
            self.msg("你想拿什麼？")
            return

        objs = caller.search(
            self.args,
            location=caller.location,
            nofound_string=f"這裡沒有「{self.args}」。",
            multimatch_string=f"這裡有多個「{self.args}」，請指定其中一個：",
            stacked=self.number,
        )
        if not objs:
            return
        objs = utils.make_iter(objs)

        if len(objs) == 1 and caller == objs[0]:
            self.msg("你不能拿起自己。")
            return

        for obj in objs:
            if not obj.access(caller, "get"):
                self.msg(obj.db.get_err_msg or "你不能拿那個。")
                return
            if not obj.at_pre_get(caller):
                return

        moved = []
        for obj in objs:
            if obj.move_to(caller, quiet=True, move_type="get"):
                moved.append(obj)
                obj.at_get(caller)

        if not moved:
            self.msg("那個拿不起來。")
        else:
            obj_name = _counted_name(moved[0], len(moved), caller)
            caller.msg(f"你拿起了 {obj_name}。")
            if caller.location:
                caller.location.msg_contents(
                    f"{_name(caller)} 拿起了 {obj_name}。", exclude=caller
                )


class CmdDrop(general.CmdDrop):
    """
    放下身上的物品。

    用法:
      放下 <物品>
      drop <object>
    """

    aliases = ["放下", "丟下", "丟", "放"]
    help_category = "一般"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("你想放下什麼？")
            return

        objs = caller.search(
            self.args,
            location=caller,
            nofound_string=f"你身上沒有「{self.args}」。",
            multimatch_string=f"你身上有多個「{self.args}」，請指定其中一個：",
            stacked=self.number,
        )
        if not objs:
            return
        objs = utils.make_iter(objs)

        for obj in objs:
            if not obj.at_pre_drop(caller):
                return

        moved = []
        for obj in objs:
            if obj.move_to(caller.location, quiet=True, move_type="drop"):
                moved.append(obj)
                obj.at_drop(caller)

        if not moved:
            self.msg("那個無法放下。")
        else:
            obj_name = _counted_name(moved[0], len(moved), caller)
            caller.msg(f"你放下了 {obj_name}。")
            if caller.location:
                caller.location.msg_contents(
                    f"{_name(caller)} 放下了 {obj_name}。", exclude=caller
                )


class CmdGive(general.CmdGive):
    """
    把身上的物品交給別人。

    用法:
      給 <物品> = <對象>
      給 <物品> 給 <對象>
      give <object> = <target>
    """

    aliases = ["給", "交給", "給予"]
    rhs_split = ("=", " to ", " 給 ", "給")
    help_category = "一般"

    def func(self):
        caller = self.caller
        if not self.args or not self.rhs:
            caller.msg("用法：給 <身上物品> = <對象>")
            return

        to_give = caller.search(
            self.lhs,
            location=caller,
            nofound_string=f"你身上沒有「{self.lhs}」。",
            multimatch_string=f"你身上有多個「{self.lhs}」，請指定其中一個：",
            stacked=self.number,
        )
        if not to_give:
            return

        target = caller.search(
            self.rhs,
            nofound_string=f"找不到「{self.rhs}」。",
            multimatch_string=f"找到多個「{self.rhs}」，請指定其中一個：",
        )
        if not target:
            return

        to_give = utils.make_iter(to_give)
        obj_name = _counted_name(to_give[0], len(to_give), caller)

        if target == caller:
            caller.msg(f"你把 {obj_name} 留給自己。")
            return

        for obj in to_give:
            if not obj.at_pre_give(caller, target):
                return

        moved = []
        for obj in to_give:
            if obj.move_to(target, quiet=True, move_type="give"):
                moved.append(obj)
                obj.at_give(caller, target)

        if not moved:
            caller.msg(f"你無法把 {obj_name} 交給 {_name(target, caller)}。")
        else:
            obj_name = _counted_name(to_give[0], len(moved), caller)
            caller.msg(f"你把 {obj_name} 交給 {_name(target, caller)}。")
            target.msg(f"{_name(caller, target)} 把 {obj_name} 交給你。")


class CmdSetDesc(general.CmdSetDesc):
    """
    設定自己的描述。

    用法:
      描述 <描述文字>
      setdesc <description>
    """

    aliases = ["描述", "自介", "設定描述"]
    help_category = "一般"

    def func(self):
        if not self.args:
            self.msg("請輸入一段描述。")
            return
        self.caller.db.desc = self.args.strip()
        self.msg("你更新了自己的描述。")


class CmdSay(general.CmdSay):
    """
    對同一地點的人說話。

    用法:
      說 <訊息>
      say <message>
    """

    aliases = ['"', "'", "說", "講", "說話"]
    help_category = "一般"

    def func(self):
        if not self.args:
            self.caller.msg("你想說什麼？")
            return
        speech = self.caller.at_pre_say(self.args)
        if speech:
            self.caller.at_say(speech, msg_self=True)


class CmdWhisper(general.CmdWhisper):
    """
    對一個或多個角色悄悄說話。

    用法:
      密語 <角色> = <訊息>
      whisper <character> = <message>
    """

    aliases = ["密語", "悄悄說", "耳語"]
    help_category = "一般"

    def func(self):
        caller = self.caller
        if not self.lhs or not self.rhs:
            caller.msg("用法：密語 <角色> = <訊息>")
            return

        receivers = [
            caller.search(
                receiver.strip(),
                nofound_string=f"找不到「{receiver.strip()}」。",
                multimatch_string=f"找到多個「{receiver.strip()}」，請指定其中一個：",
            )
            for receiver in set(self.lhs.split(","))
        ]
        receivers = [recv for recv in receivers if recv]
        speech = self.rhs
        if not speech or not receivers:
            return

        speech = caller.at_pre_say(speech, whisper=True, receivers=receivers)
        msg_self = None if caller in receivers else True
        caller.at_say(speech, msg_self=msg_self, receivers=receivers, whisper=True)


class CmdPose(general.CmdPose):
    """
    做出一段動作描述。

    用法:
      動作 <描述>
      pose <text>
    """

    aliases = [":", "emote", "動作", "姿態", "表情"]
    help_category = "一般"

    def func(self):
        if not self.args:
            self.msg("你想做什麼？")
        else:
            msg = f"{self.caller.name}{self.args}"
            self.caller.location.msg_contents(text=(msg, {"type": "pose"}), from_obj=self.caller)


class CmdHelp(help_cmds.CmdHelp):
    """
    查看幫助。

    用法:
      幫助
      幫助 <主題或指令>
      help <topic>
    """

    aliases = ["?", "幫助", "說明", "help"]
    help_category = "一般"

    def format_help_entry(self, *args, **kwargs):
        text = super().format_help_entry(*args, **kwargs)
        return (
            text.replace("Help for", "說明：")
            .replace("No help found", "找不到說明")
            .replace("Subtopics:", "子主題：")
            .replace("Other topic suggestions:", "你可能也想看：")
            .replace("aliases:", "別名：")
        )


class CmdCharCreate(account.CmdCharCreate):
    aliases = ["創角", "建立角色", "新增角色"]
    help_category = "一般"

    def func(self):
        if not self.args:
            self.msg("用法：創角 <角色名> [= 描述]")
            return

        key = self.lhs
        description = self.rhs or "這是一名新角色。"
        new_character, errors = self.account.create_character(
            key=key, description=description, ip=self.session.address
        )
        if errors:
            self.msg(errors)
        if new_character:
            self.msg(f"已建立角色 {new_character.key}。輸入 |wic {new_character.key}|n 進入遊戲。")


class CmdIC(account.CmdIC):
    aliases = ["puppet", "進入", "扮演", "進遊戲"]
    help_category = "一般"

    def func(self):
        if not self.args and not self.account.db._last_puppet:
            self.msg("用法：進入 <角色名>")
            return
        super().func()


class CmdOOC(account.CmdOOC):
    aliases = ["unpuppet", "離開角色", "出戲"]
    help_category = "一般"

    def func(self):
        old_char = self.account.get_puppet(self.session)
        if not old_char:
            self.msg("你已經在角色外狀態。")
            return

        self.account.db._last_puppet = old_char
        try:
            self.account.unpuppet_object(self.session)
            self.msg("你暫時離開了角色。")
        except RuntimeError as exc:
            self.msg(f"|r無法離開角色 |c{old_char}|n：{exc}")


class CmdWho(account.CmdWho):
    aliases = ["doing", "誰", "在線", "線上"]
    help_category = "一般"

    def func(self):
        sessions = [session for session in evennia.SESSION_HANDLER.get_sessions() if session.logged_in]
        names = []
        for session in sessions:
            acc = session.get_account()
            if acc:
                names.append(acc.get_display_name(self.account))
        if not names:
            self.msg("目前沒有帳號在線。")
        else:
            self.msg("目前在線：\n  " + "\n  ".join(sorted(set(names))))


class CmdQuit(account.CmdQuit):
    aliases = ["q", "qu", "離開", "退出", "斷線"]
    help_category = "一般"

    def func(self):
        account_obj = self.account
        if "all" in self.switches:
            account_obj.msg("|R離線|n：正在中斷所有連線。", session=self.session)
            for session in account_obj.sessions.all():
                account_obj.disconnect_session_from_account(session, "quit/all")
        else:
            account_obj.msg("|R離線|n：期待下次再見。", session=self.session)
            account_obj.disconnect_session_from_account(self.session, "quit")


class CmdUnconnectedConnect(unloggedin.CmdUnconnectedConnect):
    aliases = ["conn", "con", "co", "登入", "連線", "連接"]

    def func(self):
        if not self.args:
            self.caller.msg("用法：登入 <帳號> <密碼>")
            return
        super().func()


class CmdUnconnectedCreate(unloggedin.CmdUnconnectedCreate):
    aliases = ["cre", "cr", "註冊", "建立", "創建"]

    def at_pre_cmd(self):
        if not settings.NEW_ACCOUNT_REGISTRATION_ENABLED:
            self.msg("目前不開放註冊新帳號。")
            return True
        return False

    def func(self):
        session = self.caller
        args = self.args.strip()

        Account = class_from_module(settings.BASE_ACCOUNT_TYPECLASS)

        parts = [part.strip() for part in re.split(r"\"", args) if part.strip()]
        if len(parts) == 1:
            parts = parts[0].split(None, 1)
        if len(parts) != 2:
            session.msg("用法：註冊 <帳號> <密碼>。若帳號或密碼含空白，請用雙引號包起來。")
            return

        username, password = parts
        non_normalized_username = username
        username = Account.normalize_username(username)
        if non_normalized_username != username:
            session.msg("注意：帳號名稱已自動整理，移除了空白或容易混淆的字元。")

        answer = yield f"你要建立帳號「{username}」，密碼為「{password}」。確認嗎？[Y]/N"
        if answer.lower() in ("n", "no", "否", "不"):
            session.msg("已取消。若帳號名稱含空白，請用雙引號包起來。")
            return

        new_account, errors = Account.create(
            username=username, password=password, ip=session.address, session=session
        )
        if new_account:
            if " " in username:
                login = f'登入 "{username}" <你的密碼>'
            else:
                login = f"登入 {username} <你的密碼>"
            session.msg(f"新帳號「{username}」已建立。歡迎！\n\n你現在可以用以下指令登入：|w{login}|n")
        else:
            session.msg("|R%s|n" % "\n".join(errors))


class CmdUnconnectedQuit(unloggedin.CmdUnconnectedQuit):
    aliases = ["q", "qu", "離開", "退出", "斷線"]

    def func(self):
        self.caller.sessionhandler.disconnect(self.caller, "再見，連線已中斷。")


class CmdUnconnectedLook(unloggedin.CmdUnconnectedLook):
    aliases = ["look", "l", "看", "畫面"]


class CmdUnconnectedHelp(unloggedin.CmdUnconnectedHelp):
    aliases = ["h", "?", "幫助", "說明"]

    def func(self):
        self.msg(
            """
你還沒有登入遊戲。目前可用的指令：

  |w註冊 <帳號> <密碼>|n - 建立新帳號
  |w登入 <帳號> <密碼>|n - 登入既有帳號
  |w看|n - 重新顯示連線畫面
  |w幫助|n - 顯示這份說明
  |w離開|n - 中斷連線

英文指令也仍可使用：|wcreate|n、|wconnect|n、|wlook|n、|whelp|n、|wquit|n。
"""
        )
