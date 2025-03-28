import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QDialog, QTableWidgetItem, \
    QMessageBox, QLineEdit, QCheckBox
from PyQt6.QtCore import pyqtSignal
from ui_compiled.main_window import Ui_MainWindow
from ui_compiled.settings_window import Ui_Dialog
from misc.db import *


class SettingsWindow(QDialog):
    settings_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


        self.ui.btnSave.setDefault(True)
        self.ui.btnCancel.setAutoDefault(False)

        self.env_data = get_env_settings()
        self.inputs = {}
        self.load_env_parameters()

        self.ui.btnSave.clicked.connect(self.save_settings)
        self.ui.btnCancel.clicked.connect(self.confirm_close)

    def load_env_parameters(self):
        layout = self.ui.verticalLayout

        for param, value in self.env_data:
            label = QLabel(param)
            layout.addWidget(label)

            if value.lower() in ("true", "false"):
                input_widget = QCheckBox()
                input_widget.setChecked(value.lower() == "true")
            else:
                input_widget = QLineEdit(value)

            layout.addWidget(input_widget)
            self.inputs[param] = input_widget

    def save_settings(self):
        for param, input_widget in self.inputs.items():
            if isinstance(input_widget, QCheckBox):
                new_value = "True" if input_widget.isChecked() else "False"
            else:
                new_value = input_widget.text()

            set_env_param(param, new_value)

        # QMessageBox.information(self, "Успех", "Настройки сохранены!")
        self.settings_updated.emit()
        self.close()

    def confirm_close(self):
        reply = QMessageBox.question(
            self, "Подтверждение", "Закрыть без сохранения?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.open_settings)
        self.load_env_settings()

    def load_env_settings(self):
        settings = get_env_settings()
        table = self.ui.tableWidget

        table.setRowCount(len(settings))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Параметр", "Значение"])

        for row, (param, value) in enumerate(settings):
            table.setItem(row, 0, QTableWidgetItem(param))
            table.setItem(row, 1, QTableWidgetItem(value))

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.accepted.connect(self.load_env_settings)
        self.settings_window.exec()
        self.load_env_settings()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
