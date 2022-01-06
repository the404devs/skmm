import sys, json, shutil
from PyQt6.QtCore import QMimeData, QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QDrag
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMainWindow,
    QPushButton,
    QToolBar,
    QScrollArea,
    QVBoxLayout,
    QWidget
)

# TODO: detect unsaved changes


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SKMM 0.0.1")
        self.setAcceptDrops(True)
        # self.setFixedSize(800, 800)
        self.layout = QVBoxLayout()

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        toolbar = QToolBar("My main toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        button_config = QAction("Config", self)
        button_config.setStatusTip("Configure SKMM")
        toolbar.addAction(button_config)
        # TODO: Add config dialog

        button_refresh = QAction("Refresh", self)
        button_refresh.setStatusTip("Refresh mod list, adding new ESPs not yet listed.")
        toolbar.addAction(button_refresh)
        # TODO: Add refresh function

        button_config = QAction("Save", self)
        button_config.setStatusTip("Save current mod list")
        toolbar.addAction(button_config)
        button_config.triggered.connect(self.save)

        button_config = QAction("About", self)
        button_config.setStatusTip("About SKMM")
        toolbar.addAction(button_config)
        # TODO: Add about dialog
        # button_action.triggered.connect(self.onMyToolBarButtonClick)
        self.setGeometry(600, 100, 600, 900)
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setCentralWidget(self.scroll)
        self.show()

    def dragEnterEvent(self, e):
        e.accept()
    
    def dropEvent(self, e):
        pos = e.position()
        widget = e.source()
        for n in range(self.layout.count()):
            # Get the widget at each index in turn.
            w = self.layout.itemAt(n).widget()
            if pos.y() + window.scroll.verticalScrollBar().value() <= w.y() + w.size().height() // 2:
                # We didn't drag past this widget.
                # insert to the left of it.
                self.layout.insertWidget(n-1, widget)
                break

        e.accept()

    def save(self):
        print("Saving mod list...")
        path = config.get("PluginPath")
        shutil.copy(path, path + ".bak")
        print("Previous mod list backed up to: " + path + ".bak")
        with open(path, "w") as f:
            for n in range(self.layout.count()):
                w = self.layout.itemAt(n).widget()
                if isinstance(w, ModBar):
                    f.write(("*" if w.button.property("mod_enabled") else "") + w.button.text() + "\n")

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
        self.button.width = 50
        self.button.setProperty("mod_enabled", value)
        self.button.setStyleSheet("color: " + color)
        self.button.clicked.connect(self.toggle)

        self.label = QLabel("Drag 🡙")
        self.label.setFixedSize(QSize(50, 50))
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def toggle(self):
        self.button.setProperty("mod_enabled", not self.button.property("mod_enabled"))
        self.button.setStyleSheet("color: " + ("#00ff00" if self.button.property("mod_enabled") else "#ff0000"))
        print(self.button.text() + " is now: " + str(self.button.property("mod_enabled")))
        print(window.scroll.verticalScrollBar().value())

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec(Qt.DropAction.MoveAction)

def parse_config():
    with open("./config.json") as f:
        return json.load(f)

def populate_ui():
    plugin_path = config.get("PluginPath")
    print("Current path to Plugins.txt: " + plugin_path)
    arr = []
    with open(plugin_path) as f:
        for line in f:
            arr.append(line.strip())
            bar = ModBar(line.strip())
            window.layout.addWidget(bar)
    dummy = QLabel(" ")
    dummy.setFixedHeight(5)
    window.layout.addWidget(dummy)

config = parse_config()
app = QApplication(sys.argv)

window = MainWindow()
window.show()
populate_ui()

app.exec()