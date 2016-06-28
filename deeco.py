import random
import math

from runnable import Runnable
from sim import Sim
from sim import Scheduler


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

	def run(self, scheduler: Scheduler):
		for component in self.components:
			component.run(scheduler)


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
	def gen_id():
		identifier = Component.counter
		Component.counter += 1
		return identifier

	def __init__(self, node: Node):
		node.add_component(self)

		self.time = None
		self.node = node
		self.knowledge = Knowledge()
		self.metadata = Metadata()

		self.id = self.gen_id()

	def process_factory(self, entry):
		return lambda time_ms: entry(self, self.knowledge)

	def run(self, scheduler):
		for entry in type(self).__dict__.values():
			if hasattr(entry, "is_process"):
				method = self.process_factory(entry)
				scheduler.set_periodic_timer(method, 1000)