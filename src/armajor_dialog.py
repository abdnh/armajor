import sys

# pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog, QApplication, QShortcut  # type: ignore
from PyQt5.QtGui import QKeySequence  # type: ignore

if __name__ == "__main__":
    import dialog as armjaor_form  # type: ignore # pylint: disable=import-error
    from armajor import ArabicMnemonicMajor  # type: ignore # pylint: disable=import-error
else:
    from . import dialog as armjaor_form
    from .armajor import ArabicMnemonicMajor


class ArMajorDialog(QDialog):
    def __init__(
        self,
        parent,
        major: ArabicMnemonicMajor,
        search_text: str = "",
        word_to_num_checked: bool = False,
    ):
        QDialog.__init__(self, parent)
        self.form = armjaor_form.Ui_Dialog()
        self.form.setupUi(self)

        self.form.lineEdit.setFocus()
        self.form.lineEdit.setText(search_text)
        self.form.searchButton.clicked.connect(self.accept) # type: ignore
        self.form.copySelectedButton.clicked.connect(self.on_copy_selected) # type: ignore
        focusSearchHotkey = QShortcut(QKeySequence("Ctrl+F"), self)
        focusSearchHotkey.activated.connect(self.form.lineEdit.setFocus) # type: ignore
        self.form.wordToNum.toggled.connect(self.on_mode_changed) # type: ignore
        self.form.wordToNum.setChecked(word_to_num_checked)
        changeModeHotkey = QShortcut(QKeySequence("Ctrl+W"), self)
        changeModeHotkey.activated.connect(self.toggle_mode) # type: ignore

        self.major = major
        if search_text.strip():
            self.accept()

    def accept(self):
        self.form.listWidget.clear()
        if self.form.wordToNum.isChecked():
            self.on_number_lookup()
        else:
            self.on_word_lookup()
        if self.form.listWidget.count():
            self.form.listWidget.setFocus()
            self.form.listWidget.setCurrentRow(0)

    def on_word_lookup(self):
        try:
            self.form.listWidget.addItems(self.major.lookup(self.form.lineEdit.text()))
        except ValueError:
            pass

    def on_number_lookup(self):
        word = self.major.word_to_num(self.form.lineEdit.text())
        if word:
            self.form.listWidget.addItem(word)

    def on_copy_selected(self):
        selected_items = self.form.listWidget.selectedItems()
        selected_text = []
        for item in selected_items:
            selected_text.append(item.text())
        QApplication.clipboard().setText("\n".join(selected_text) + "\n")

    def on_mode_changed(self):
        if self.form.wordToNum.isChecked():
            self.form.lineEdit.setPlaceholderText("أدخل كلمة")
        else:
            self.form.lineEdit.setPlaceholderText("أدخل رقمًا")

    def toggle_mode(self):
        self.form.wordToNum.setChecked(not self.form.wordToNum.isChecked())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    major = ArabicMnemonicMajor("words.txt")
    d = ArMajorDialog(None, major)
    d.exec_()
