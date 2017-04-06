from core.runnable import *
from core.packets import KnowledgePacket

class Node(Runnable):
	counter = 0

	@staticmethod
	def __gen_id():
		identifier = Node.counter
		Node.counter += 1
		return identifier

	def __init__(self, runtime: Runtime):
		runtime.add_node(self)

		self.runtime = runtime
		self.id = self.__gen_id()

		self.plugins = []
		self.components = []

		# Deploy system plugins on node
		for plugin in runtime.plugins:
			plugin.attach_to(self)

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
					method = process_factory(component, entry, self)
					scheduler.set_periodic_timer(method, entry.period_ms)


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


def process(period_ms: int):
	def process_with_period(method):
		method.is_process = True
		method.period_ms = period_ms
		return method

	return process_with_period


def process_factory(component, entry, node: Node):
	return lambda time_ms: entry(component, node)


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

		self.time = None
		self.knowledge = self.Knowledge()
		self.knowledge.id = self.id
		self.metadata = Metadata()

#
# class Ensemble:
# 	def membership(self):
# 		pass
#
# 	def fitness(self):
# 		pass
#
# 	def exchange(self):
# 		pass


class ShadowKnowledge:
	def __init__(self, packet: KnowledgePacket):
		self.__init__(packet.id)
		self.timestamp = packet.timestamp_ms
		self.knowledge = packet.knowledge

	# TODO: Unused ?
	def __init__(self, component_id: int):
		self.id = component_id
		self.timestamp = 0
		self.knowledge = None

	def update(self, knowledge: Component.Knowledge, time):
		if self.timestamp < time:
			self.knowledge = knowledge
			self.timestamp = time


class EnsembleDefinition:
	def fitness(self, *knowledge):
		pass

	def membership(self, *knowledge):
		pass

	def knowledge(self, *knowledge):
		pass


class EnsembleInstance:
	def __init__(self, definition: EnsembleDefinition):
		self.definition = definition
		self.memberKnowledge = []

	def fitness(self):
		self.definition.fitness(self.memberKnowledge)

	def knowledge(self):
		self.definition.knowledge(self.memberKnowledge)

	def add_impact(self, knowledge: ShadowKnowledge):
		# TODO: calculate fitness change when knowledge si added
		return 42

	def remove_impact(self, knowledge: ShadowKnowledge):
		# TODO: calculate fitness change when knowledge si removed
		return -42

	def replace_impact(self, knowledge: ShadowKnowledge):
		# TODO: calculate fitness change when knowledge si replaced
		return 0
