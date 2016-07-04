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
			for entry in type(component).__dict__.values():
				if hasattr(entry, "is_process"):
					method = process_factory(component, entry)
					scheduler.set_periodic_timer(method, 1000)


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


class BaseKnowledge(Identifiable, TimeStamped):
	def __init__(self):
		super().__init__()


class Metadata:
	def __init__(self):
		self.coordinatedBy = None
		self.coordinating = None


def process(method):
		method.is_process = True
		return method


def process_factory(component, entry):
	return lambda time_ms: entry(component, component.knowledge)


class Component:
	counter = 0

	class Knowledge:
		pass

	@staticmethod
	def gen_id():
		identifier = Component.counter
		Component.counter += 1
		return identifier

	def __init__(self, node: Node):
		self.id = self.gen_id()
		node.add_component(self)

		self.time = None
		self.node = node
		self.knowledge = self.Knowledge()
		self.knowledge.id = self.id
		self.metadata = Metadata()
