import random
import math

from runnable import Runnable
from sim import Sim


class Node(Runnable):
	counter = 0

	def __init__(self, runtime: Sim):
		runtime.add_runnable(self)

		self.runtime = runtime
		self.id = Node.counter
		Node.counter += 1

		self.components = []

	def add_component(self, component):
		self.components.append(component)

	def do_step(self, time):
		# Run components
		for component in self.components:
			component.do_step(time)


class Knowledge:
	pass


class Metadata:
	def __init__(self):
		self.coordinatedBy = None
		self.coordinating = None


def process(method):
		method.is_process = True
		return method


class Component(Runnable):
	counter = 0

	@staticmethod
	def genid():
		id = Component.counter
		Component.counter += 1
		return id

	def __init__(self, node: Node):
		node.add_component(self)

		self.time = None
		self.node = node
		self.knowledge = Knowledge()
		self.metadata = Metadata()

		self.knowledge.id = Component.genid()

	def do_step(self, time):
		self.time = time

		# Run "processes"
		for entry in type(self).__dict__.values():
			if hasattr(entry, "is_process"):
				entry(self, self.knowledge)
