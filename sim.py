import jsonpickle as json
import os
from runnable import Runnable


class Sim:
	def __init__(self, snapshot_dir = None):
		self.runnables = []
		self.snapshot_dir = snapshot_dir
		self.time = 0

		if snapshot_dir is not None:
			try:
				os.mkdir(self.snapshot_dir)
			except FileExistsError as e:
				pass

	def add_runnable(self, runnable: Runnable):
		self.runnables.append(runnable)

	def run(self, limit: int):
		for time in range(0, limit):
			self.time = time

			# Run nodes
			for node in self.runnables:
				node.do_step(time)

			# Snapshot the system
			if self.snapshot_dir is not None:
				log = open(self.snapshot_dir + os.sep + str(time) + ".json", "w")
				dump = json.encode(self)
				log.write(dump)
				log.close()