import sys, json
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SKMM 0.0.1")
        self.setFixedSize(800, 800)
        self.layout = QVBoxLayout()

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
        self.show()

class ModBar(QWidget):
    def __init__(self, str):
        super().__init__()
        # self.setContentsMargins(0, 0, 0, 0)
        # self.setSpacing(0)
        self.layout = QHBoxLayout()
        name = str
        color = "#ff0000"
        value = False
        if str.startswith("*"):
            name = str[1:]
            color = "#00ff00"
            value = True
        self.button = QPushButton(name)
        self.button.setProperty("mod_enabled", value)
        self.button.setStyleSheet("color: " + color)
        self.button.clicked.connect(self.toggle)

        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def toggle(self):
        self.button.setProperty("mod_enabled", not self.button.property("mod_enabled"))
        self.button.setStyleSheet("color: " + ("#00ff00" if self.button.property("mod_enabled") else "#ff0000"))
        print(self.button.text() + " is now: " + str(self.button.property("mod_enabled")))

def parse_config():
    with open("./config.json") as f:
        return json.load(f)

def populate_ui():
    config = parse_config()
    plugin_path = config.get("PluginPath")
    print("Current path to Plugins.txt: " + plugin_path)
    arr = []
    with open(plugin_path) as f:
        for line in f:
                arr.append(line.strip())
                bar = ModBar(line.strip())
                window.layout.addWidget(bar)
        # print(arr)



app = QApplication(sys.argv)

window = MainWindow()
window.show()
populate_ui()

app.exec()