import sys

# pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog, QApplication, QShortcut  # type: ignore
from PyQt5.QtGui import QKeySequence  # type: ignore

if __name__ == "__main__":
    import dialog as armjaor_form  # type: ignore
    from armajor import ArabicMnemonicMajor  # type: ignore
else:
    from . import dialog as armjaor_form
    from .armajor import ArabicMnemonicMajor


class ArMajorDialog(QDialog):
    def __init__(self, parent, words_filename: str, search_text: str = ""):
        QDialog.__init__(self, parent)
        self.form = armjaor_form.Ui_Dialog()
        self.form.setupUi(self)

        self.form.lineEdit.setFocus()
        self.form.lineEdit.setText(search_text)
        self.form.searchButton.clicked.connect(self.accept)
        self.form.copySelectedButton.clicked.connect(self.on_copy_selected)
        focusSearchHotkey = QShortcut(QKeySequence("Ctrl+F"), self)
        focusSearchHotkey.activated.connect(self.form.lineEdit.setFocus)

        self.major = ArabicMnemonicMajor(words_filename)

    def accept(self):
        self.form.listWidget.clear()
        try:
            self.form.listWidget.addItems(self.major.lookup(self.form.lineEdit.text()))
        except ValueError:
            pass

    def on_copy_selected(self):
        selected_items = self.form.listWidget.selectedItems()
        selected_text = []
        for item in selected_items:
            selected_text.append(item.text())
        QApplication.clipboard().setText("\n".join(selected_text) + "\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = ArMajorDialog(None, "words.txt")
    d.exec_()
