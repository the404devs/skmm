import os, sys, json, shutil
from PyQt6.QtCore import QMimeData, QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QDrag, QWindow
from PyQt6.QtWidgets import (
	QApplication,
	QFormLayout,
	QHBoxLayout,
	QLabel,
	QLayout,
	QLineEdit,
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

		toolbar = QToolBar()
		toolbar.setMovable(False)
		self.addToolBar(toolbar)

		button_config = QAction("Config", self)
		button_config.setToolTip("Configure SKMM")
		toolbar.addAction(button_config)
		button_config.triggered.connect(self.configClicked)

		button_refresh = QAction("Refresh", self)
		button_refresh.setToolTip("Refresh mod list, adding new ESPs not yet listed.")
		toolbar.addAction(button_refresh)
		# TODO: Add refresh function

		button_save = QAction("Save", self)
		button_save.setToolTip("Save current mod list")
		toolbar.addAction(button_save)
		button_save.triggered.connect(self.save)

		button_about = QAction("About", self)
		button_about.setToolTip("About SKMM")
		toolbar.addAction(button_about)
		# TODO: Add about dialog
		button_about.triggered.connect(genocide)
		self.setGeometry(600, 100, 610, 900)
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
				self.layout.insertWidget(n-1, widget)
				break
		numbering()
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

	def configClicked(self):
		print("Config clicked")
		self.config_dialog = ConfigDialog(config)
		# config_dialog.show()

class ModBar(QWidget):
	def __init__(self, str):
		super().__init__()
		self.layout = QHBoxLayout()
		name = str
		color = "#ff0000"
		value = False
		if str.startswith("*"):
			name = str[1:]
			color = "#00ff00"
			value = True

		self.num_label = QLabel("")
		self.num_label.setFixedSize(QSize(25, 20))
		self.num_label.setAlignment(Qt.AlignmentFlag.AlignRight)
		self.layout.addWidget(self.num_label)

		self.button = QPushButton(name)
		self.button.width = 50
		self.button.setProperty("mod_enabled", value)
		self.button.setStyleSheet("color: " + color)
		self.button.clicked.connect(self.toggle)
		self.layout.addWidget(self.button)

		self.drag_label = QLabel(" 🡙")
		self.drag_label.setToolTip("Drag to reorder")
		self.drag_label.setFixedSize(QSize(50, 50))
		self.layout.addWidget(self.drag_label)

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

class ConfigDialog(QWidget):
	# TODO: Add user-friendly tooltips, filepickers
	def __init__(self, config):
		super().__init__()
		layout = QFormLayout()
		self.config = config
		self.setWindowTitle("SKMM Config")
		self.setGeometry(600, 100, 610, 450)
		qr = self.frameGeometry()
		cp = self.screen().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		self.setLayout(layout)

		label1 = QLabel("Plugin Path:")
		layout.addWidget(label1)
		self.plugin_line = QLineEdit()
		self.plugin_line.setText(config.get("PluginPath") or "")
		layout.addWidget(self.plugin_line)

		label2 = QLabel("Data Path:")
		layout.addWidget(label2)
		self.data_line = QLineEdit()
		self.data_line.setText(config.get("DataPath"))
		layout.addWidget(self.data_line)

		save_button = QPushButton("Save")
		save_button.clicked.connect(self.save)
		layout.addWidget(save_button)

		self.show()

	def save(self):
		print(self.config.get("PluginPath"))
		print("Saving config...")
		self.config["PluginPath"] = self.plugin_line.text()
		self.config["DataPath"] = self.data_line.text()
		json.dump(self.config, open("config.json", "w"), indent=4)
		print("Config saved.")
		config = parse_config()
		genocide()
		populate_ui()
		self.close()


def parse_config():
	path = "./config.json"
	if not os.path.exists(path):
		print("No config file found, creating one...")
		with open(path, "w") as f:
			f.write("{}")
	with open(path) as f:
		return json.load(f)

def populate_ui():
	plugin_path = config.get("PluginPath")
	if not plugin_path:
		warning = QLabel("No plugin path is set.\nTell SKMM where to find Plugins.txt in the Config menu.")
		warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
		window.layout.addWidget(warning)
	else:
		print("Current path to Plugins.txt: " + plugin_path)
		arr = []
		with open(plugin_path) as f:
			for line in f:
				arr.append(line.strip())
				bar = ModBar(line.strip())
				window.layout.addWidget(bar)
		numbering()
		dummy = QLabel(" ")
		dummy.setFixedHeight(5)
		window.layout.addWidget(dummy)

def genocide():
	for n in reversed(range(window.layout.count())):
		window.layout.itemAt(n).widget().setParent(None)

def numbering():
	for n in range(window.layout.count()):
		w = window.layout.itemAt(n).widget()
		if isinstance(w, ModBar):
			w.num_label.setText(str(n))

config = parse_config()
app = QApplication(sys.argv)
window = MainWindow()
populate_ui()

app.exec()