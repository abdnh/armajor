import os
from typing import List

from aqt import mw, gui_hooks
from aqt.qt import QAction
from aqt.editor import Editor

from .armajor_dialog import ArMajorDialog

addon_dir = os.path.dirname(__file__)
words_filename = os.path.join(addon_dir, "words.txt")


def open_dialog(parent, search_text=""):
    dialog = ArMajorDialog(parent, words_filename, search_text)
    dialog.exec_()


def open_dialog_in_editor(editor: Editor):
    def cb(selected):
        open_dialog(editor.widget, selected)

    editor.web.evalWithCallback("window.getSelection().toString()", cb)


def on_editor_did_init_buttons(buttons: List[str], editor: Editor):
    btn = editor.addButton(
        icon=os.path.join(addon_dir, "icon.svg"),
        cmd="armajor",
        func=open_dialog_in_editor,
        tip="مولد نظام المذكرات الصوتي للعربية",
        keys="Ctrl+Shift+A",
    )

    buttons.append(btn)


action = QAction(mw)
action.setText("مولد نظام المذكرات الصوتي للعربية")
mw.form.menuTools.addAction(action)
action.triggered.connect(lambda: open_dialog(mw))

gui_hooks.editor_did_init_buttons.append(on_editor_did_init_buttons)
