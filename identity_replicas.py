import copy

from runnable import SimPlugin
from deeco import Node


class IdentityReplicas(SimPlugin):
	def __init__(self, sim):
		super().__init__(sim)
		self.nodes = []

	def attach_to(self, node: Node):
		self.nodes.append(node)
		node.replicas = self

	def get(self, knowledge_type):
		matching_knowledge = []

		for node in self.nodes:
			for component in node.components:
				if set(component.knowledge.__class__.__bases__) >= set(knowledge_type.__bases__):
					matching_knowledge.append(copy.deepcopy(component.knowledge))

		return matching_knowledge
