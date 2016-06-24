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

colors = ["red", "green", "blue", "yellow", "black", "lime", "cyan", "orange", "orange", "orange", "orange"]


class PlottingCanvas(FigureCanvas):
	def __init__(self, logs, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.plot = self.fig.add_subplot(1, 1, 1)
		self.log = logs.log
		self.final = logs.final

		self.drawPlot(0)

		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def drawPlot(self, recNum):
		rec = self.log[recNum]

		self.plot.clear()
		self.plotRecord(rec)

		self.plot.set_title("Time: " + str(rec.time) + " ms")
		self.plot.set_xlim(0, 1)
		self.plot.set_ylim(0, 1)

	def plotRecord(self, rec):
		for component in rec.components:
			self.plot.plot(component.position.x, component.position.y, "g^")



	def updatePlot(self, recNum):
		self.drawPlot(recNum)
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

		slider.valueChanged.connect(drawing.updatePlot)
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