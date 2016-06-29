import random
import math

from runnable import *


class Node(Runnable):
	counter = 0

	@staticmethod
	def gen_id():
		identifier = Node.counter
		Node.counter += 1
		return identifier

	def __init__(self, runtime: Runtime):
		runtime.add_node(self)

		self.runtime = runtime
		self.id = self.gen_id()

		self.plugins = []
		self.components = []
		self.replicas = []

	def add_component(self, component):
		self.components.append(component)

	def add_plugin(self, plugin: NodePlugin):
		self.plugins.append(plugin)

	def run(self, scheduler):
		# schedule plugins
		for plugin in self.plugins:
			plugin.run(scheduler)

		# schedule component (processes)
		for component in self.components:
			component.run(scheduler)


class Role:
	pass


class Identifiable(Role):
	def __init__(self):
		super().__init__()
		self.id = None


class TimeStamped(Role):
	def __init__(self):
		super().__init__()
		self.time = None


class Knowledge(Identifiable, TimeStamped):
	def __init__(self):
		super().__init__()


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
		self.knowledge = None
		self.metadata = Metadata()

		self.id = self.gen_id()

	def process_factory(self, entry):
		return lambda time_ms: entry(self, self.knowledge)

	def run(self, scheduler):
		for entry in type(self).__dict__.values():
			if hasattr(entry, "is_process"):
				method = self.process_factory(entry)
				scheduler.set_periodic_timer(method, 1000)