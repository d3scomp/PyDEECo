from component import Component
import jsonpickle as json
import os

class Sim:
	def __init__(self, snapshot_dir = None):
		self.components = []
		self.snapshot_dir = snapshot_dir
		self.time = 0

		if not snapshot_dir is None:
			try:
				os.mkdir(self.snapshot_dir)
			except:
				pass

	def addcomponent(self, component: Component):
		self.components.append(component)

	def run(self, limit: int):
		for time in range(0, limit):
			self.time = time

			# Run components
			for component in self.components:
				component.sim_step(time)

			# Snapshot the system
			if(not self.snapshot_dir is None):
				log = open(self.snapshot_dir + os.sep + str(time) + ".json", "w")
				dump = json.encode(self)
				log.write(dump)
				log.close()