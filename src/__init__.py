import os
from typing import List
import unicodedata

# pylint: disable=import-error, no-name-in-module
# pylint: disable=invalid-name
import aqt
from aqt import gui_hooks
from aqt.qt import QAction  # type: ignore
from aqt.editor import Editor

from .armajor_dialog import ArMajorDialog
from .armajor import ArabicMnemonicMajor

addon_dir = os.path.dirname(__file__)
words_filename = os.path.join(addon_dir, "words.txt")
armajor = None


def open_dialog(parent, search_text="", word_to_num_checked: bool = False):
    global armajor  # pylint: disable=global-statement
    if not armajor:
        armajor = ArabicMnemonicMajor(words_filename)
    dialog = ArMajorDialog(parent, armajor, search_text, word_to_num_checked)
    dialog.exec_()


def contains_digit(s: str):
    for c in s:
        if unicodedata.category(c) == "Nd":
            return True
    return False


def open_dialog_in_editor(editor: Editor):
    selected = editor.web.selectedText()
    open_dialog(editor.widget, selected, not contains_digit(selected))


def on_editor_did_init_buttons(buttons: List[str], editor: Editor):
    global config  # pylint: disable=global-statement
    shortcut = config.get("shortcut", "Ctrl+Shift+K")
    btn = editor.addButton(
        icon=os.path.join(addon_dir, "icon.svg"),
        cmd="armajor",
        func=open_dialog_in_editor,
        tip=f"مولد نظام المذكرات الصوتي للعربية ({shortcut})",
        keys=shortcut,
    )

    buttons.append(btn)


if aqt.mw:
    action = QAction(aqt.mw)
    action.setText("مولد نظام المذكرات الصوتي للعربية")
    aqt.mw.form.menuTools.addAction(action)
    action.triggered.connect(lambda: open_dialog(aqt.mw))  # type: ignore
    config = aqt.mw.addonManager.getConfig(__name__)
    gui_hooks.editor_did_init_buttons.append(on_editor_did_init_buttons)
