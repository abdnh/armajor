import sys

# pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QAbstractItemView, QAbstractScrollArea, QDialog, QApplication, QHeaderView, QLabel, QShortcut, QTableWidget, QTableWidgetItem, QVBoxLayout  # type: ignore
from PyQt5.QtGui import QDesktopServices, QKeySequence  # type: ignore
from PyQt5 import QtCore

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
        self.form.searchButton.clicked.connect(self.accept)  # type: ignore
        self.form.copySelectedButton.clicked.connect(self.on_copy_selected)  # type: ignore
        self.form.showMappingsButton.clicked.connect(self.on_show_mappings)
        focusSearchHotkey = QShortcut(QKeySequence("Ctrl+F"), self)
        focusSearchHotkey.activated.connect(self.form.lineEdit.setFocus)  # type: ignore
        self.form.wordToNum.toggled.connect(self.on_mode_changed)  # type: ignore
        self.form.wordToNum.setChecked(word_to_num_checked)
        changeModeHotkey = QShortcut(QKeySequence("Ctrl+W"), self)
        changeModeHotkey.activated.connect(self.toggle_mode)  # type: ignore

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

    mappings_description = [
        "حرف الميم فيه دائرة تشبه رقم 0، وحرف الدال\nليس فوقه تنقيط يذكر بالرقم 0",
        "حرف اللام شبيه بالرقم 1، والنون والذال فوقهما\nنقطة واحدة تذكر بالرقم 1",
        "حرف الباء يرمز عادة للخيار الثاني (أ-، ب-، ت-، ...)،\nوالتاء فوقها نقطتان تذكر بالرقم 2، والثاء ملحقة بالباء والتاء",
        "حرفا العين والغين يشبهان الرقم 3، وحرفا\nالسين والشين لهما ثلاثة أسنان تذكر بالرقم 3،\nعلاوة على أن حرف الشين فوقه 3 نقاط",
        "حرف الراء يذكر بالرقم 4 لأن حرف الراء\nلا يُنطق في أي رقم إلا الرقم أربعة،\nوحرف الزاي ملحق بحرف الراء",
        "حرفا الجيم والخاء يشبهان الرقم خمسة، كما أن حرف الخاء\nلا يُنطق إلا في الرقم خمسة",
        "حرفا الطاء والظاء يشبهان الرقم 6، وحرف\nالضاد ملحق بهما",
        "حرف الحاء يشبه الرقم 7، أُلحق به حرف الصاد\nلأن حرف الحاء بقي وحيدا في بابه",
        "حرف الهاء شبيه بالرقم 8، والكاف ملحقة بالهاء\nلأنها جارتها في الترتيب الأبجدي",
        "حرف القاف يشبه الرقم 9، وحرف الفاء ملحق به",
        "بقية الحروف ملغاة، فإذا وجدت في الكلمة لا تترجم إلى رقم",
    ]

    def on_show_mappings(self):
        dlg = QDialog(self)
        dlg.setLayoutDirection(
            QtCore.Qt.RightToLeft
        )  # pylint: disable=c-extension-no-member
        dlg.setWindowTitle("جدول تحويل الأرقام إلى حروف")
        table = QTableWidget(dlg)
        mappings = self.major.mappings
        mappings[" "] = {}
        table.setColumnCount(3)
        table.setRowCount(len(mappings))
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for i, (digit, letters) in enumerate(mappings.items()):
            digit_item = QTableWidgetItem(str(digit))
            letters_item = QTableWidgetItem(", ".join(letters))
            description_item = QTableWidgetItem(self.mappings_description[i])
            table.setItem(i, 0, digit_item)
            table.setItem(i, 1, letters_item)
            table.setItem(i, 2, description_item)

        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        header = QLabel("جدول تحويل الأرقام إلى حروف", dlg)
        header.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
        )  # pylint: disable=c-extension-no-member
        font = header.font()
        font.setPointSize(font.pointSize() + 5)
        font.setBold(True)
        header.setFont(font)

        desc = QLabel(
            'مأخوذ من <a href="https://t.me/Asmaae_Kollaha">كتاب الأسماء كلها</a>', dlg
        )
        desc.setTextFormat(
            QtCore.Qt.TextFormat.RichText
        )  # pylint: disable=c-extension-no-member
        desc.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextBrowserInteraction  # pylint: disable=c-extension-no-member
        )
        desc.linkActivated.connect(
            lambda link: QDesktopServices.openUrl(
                QtCore.QUrl(link)
            )  # pylint: disable=c-extension-no-member
        )

        vbox = QVBoxLayout()
        vbox.addWidget(header)
        vbox.addWidget(desc)
        vbox.addWidget(table)
        dlg.setLayout(vbox)
        dlg.updateGeometry()

        dlg.show()

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
    d.exec()
