from node import Node

import jsonpickle as json
import os

class Sim:
	def __init__(self, snapshot_dir = None):
		self.nodes = []
		self.snapshot_dir = snapshot_dir
		self.time = 0

		if snapshot_dir is not None:
			try:
				os.mkdir(self.snapshot_dir)
			except FileExistsError as e:
				pass

	def add_node(self, node: Node):
		self.nodes.append(node)

	def run(self, limit: int):
		for time in range(0, limit):
			self.time = time

			# Run nodes
			for node in self.nodes:
				node.sim_step(time)

			# Snapshot the system
			if(not self.snapshot_dir is None):
				log = open(self.snapshot_dir + os.sep + str(time) + ".json", "w")
				dump = json.encode(self)
				log.write(dump)
				log.close()