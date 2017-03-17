from core.runnable import NodePlugin
from core.deeco import EnsembleDefinition
from core.deeco import EnsembleInstance
from core.deeco import Node
from core.deeco import ShadowKnowledge
from core.packets import Packet
from core.packets import KnowledgePacket
from core.packets import PacketType
from core.packets import DemandPacket


class ShadowRepository:
	def __init__(self):
		self.repository = {}

	def process_knowledge(self, knowledge_packet: KnowledgePacket):
		component_id = knowledge_packet.id
		if id in self.repository:
			self.repository[component_id].update(knowledge_packet.knowledge, knowledge_packet.timestamp_ms)
			return True
		else:
			return False

	def add(self, knowledge_packet: KnowledgePacket, time_ms: int):
		if self.process_knowledge(knowledge_packet):
			return False
		else:
			self.repository[knowledge_packet.id] = ShadowKnowledge(knowledge_packet)


class EnsembleReactor(NodePlugin):
	def __init__(self, node: Node, ensemble_definitions: []):
		super().__init__(node)
		self.definitions = ensemble_definitions
		self.node.networkDevice.add_receiver(self.receive)

		self.shadow_repository = ShadowRepository()
		self.instances = []

		self.demands = []

	def run(self, scheduler):
		scheduler.set_periodic_timer(self.react, period_ms=1000)

	def react(self, time_ms):
		print("Reactor invoked, sending demands")
		for demand in self.demands:
			self.node.networkDevice.broadcast(demand)

	def receive(self, packet: Packet):
		print("Packet received by reactor")
		if packet.type == PacketType.KNOWLEDGE:
			self.process_knowledge(packet)

	def process_knowledge(self, knowledge_packet: KnowledgePacket):
		print("Reactor processing knowledge packet")

		if self.shadow_repository.process_knowledge(knowledge_packet):
			# we are done, component is already handled
			return

		# TODO: Try to improve existing ensemble instance

		# Build new ensemble instance if possible
		for definition in self.definitions:
			instance = EnsembleInstance(definition)
			impact = instance.add_impact(knowledge_packet.knowledge)
			if impact >= 0:
				print("Attempting to create new ensemble instance, add impact: " + str(impact))
				demand = DemandPacket(knowledge_packet.id, self.node.id)
				self.demands.append(demand)