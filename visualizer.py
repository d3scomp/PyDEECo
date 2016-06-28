import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plot
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

import simloader
from deeco import Component
from deeco import Knowledge
from sim import Sim

colors = ["red", "green", "blue", "yellow", "black", "lime", "cyan", "orange", "orange", "orange", "orange"]


class PlottingCanvas(FigureCanvas):
	def __init__(self, logs, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.plot = self.fig.add_subplot(1, 1, 1)
		self.log = logs.log
		self.final = logs.final

		self.draw_plot(0)

		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def draw_plot(self, rec_num):
		rec = self.log[rec_num]

		self.plot.clear()
		self.plot_record(rec)

		self.plot.set_title("Time: " + str(rec.time) + " ms")
		self.plot.set_xlim(0, 1)
		self.plot.set_ylim(0, 1)

	def plot_record(self, rec: Sim):
		for node in rec.runnables:
			self.plot_node(node)

	def plot_node(self, node: Node):
		for component in node.components:
			self.plot_component(component.knowledge)

	def plot_component(self, knowledge: Knowledge):
		if knowledge.color == "red":
			self.plot.plot(knowledge.position.x, knowledge.position.y, "r^")
		elif knowledge.color == "green":
			self.plot.plot(knowledge.position.x, knowledge.position.y, "g^")
		elif knowledge.color == "blue":
			self.plot.plot(knowledge.position.x, knowledge.position.y, "b^")

	def update_plot(self, recNum):
		self.draw_plot(recNum)
		self.draw()


class Visualizer(QWidget):
	def __init__(self, logs):
		super().__init__()

		slider = QSlider(Qt.Horizontal, self)
		drawing = PlottingCanvas(logs, self, width=5, height=4, dpi=100)

		vbox = QVBoxLayout()
		vbox.addWidget(drawing)
		vbox.addWidget(slider)
		self.setLayout(vbox)

		slider.valueChanged.connect(drawing.update_plot)
		slider.setMinimum(0)
		slider.setMaximum(len(logs.log) - 1)

		self.setGeometry(150, 250, 1024, 768)
		self.setWindowTitle("Visualizer")
		self.show()


app = QApplication(sys.argv)
dirChooser = QFileDialog()
dirChooser.setFileMode(QFileDialog.DirectoryOnly)
if dirChooser.exec_() == QDialog.Accepted:
	logDir = dirChooser.selectedFiles()[0]
else:
	raise (Exception("log dir must be chosen"))

logs = simloader.load(logDir)
widget = Visualizer(logs)
app.exec_()