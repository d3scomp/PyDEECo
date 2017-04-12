from core.runnable import NodePlugin
from core.deeco import EnsembleDefinition
from core.deeco import EnsembleInstance
from core.deeco import Node
from core.deeco import ShadowKnowledge
from core.packets import Packet
from core.packets import KnowledgePacket
from core.packets import PacketType
from core.packets import DemandPacket
from core.packets import AssignmentPacket


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


class DemandRecord:
	def __init__(self, component_id: int, fitness_difference: float, target_ensemble: EnsembleInstance):
		self.component_id = component_id
		self.fitness_difference = fitness_difference
		self.target_ensemble = target_ensemble

	def __hash__(self):
		return self.component_id.__hash__()


class AssignmentRecord:
	def __init__(self, node_id: int, fitness_gain: float):
		self.node_id = node_id
		self.fitness_gain = fitness_gain


class EnsembleReactor(NodePlugin):
	def __init__(self, node: Node, ensemble_definitions: []):
		super().__init__(node)
		self.definitions = ensemble_definitions
		self.node.networkDevice.add_receiver(self.receive)

		self.shadow_repository = ShadowRepository()
		self.instances = []

		self.demands = {}

	def run(self, scheduler):
		# Add assignment records to knowledge
		for component in self.node.get_components():
			component.knowledge.assignment = AssignmentRecord(None, 0)

		scheduler.set_periodic_timer(self.react, period_ms=1000)

	def react(self, time_ms):
		print("Reactor invoked, sending demands and assignments")

		for component_id, demand in self.demands.items():
			packet = DemandPacket(time_ms, demand.component_id, self.node.id, demand.fitness_difference)
			self.node.networkDevice.broadcast(packet)

		# TODO: Maintain ensembles check timestamps

	def receive(self, packet: Packet):
		if packet.type == PacketType.KNOWLEDGE:
			self.process_knowledge(packet)

		if packet.type == PacketType.DEMAND:
			self.process_demand(packet)

		if packet.type == PacketType.ASSIGNMENT:
			self.process_assignment(packet)

	def process_knowledge(self, knowledge_packet: KnowledgePacket):
#		print("Reactor processing knowledge packet")

#		if self.shadow_repository.process_knowledge(knowledge_packet):
#			we are done, component is already handled
#			return

		if knowledge_packet.knowledge.assignment.node_id is self.node.id:
			# Already assigned to us, lets process demands
			self.process_assignment(knowledge_packet)
		else:
			# Not assigned to us, lets create demand
			self.create_demand(knowledge_packet)

	def create_demand(self, knowledge_packet: KnowledgePacket):
		# TODO: Try to improve existing ensemble instance

		# TODO: Do not create demand when fitness not better

		# Build new ensemble instance if possible
		for definition in self.definitions:
			instance = EnsembleInstance(definition)
			impact = instance.add_impact(knowledge_packet.knowledge)
			if impact >= 0:
				print("Demanding to create new ensemble instance, add impact: " + str(impact))
				demand = DemandRecord(knowledge_packet.id, impact, None)
				self.demands[knowledge_packet.id] = demand

	def process_demand(self, demand: DemandPacket):
		if demand.component_id not in map(lambda x: x.id, self.node.get_components()):
			return

		print("Reactor processing demand packet")

		assignment = self.node.get_component_by_id(demand.component_id).knowledge.assignment

		# Assign free component
		if assignment.node_id is None:
			self.assign(demand.component_id, demand.node_id, demand.fitness_difference)
			return

		# Re-assign component
		fitness_upgrade = demand.fitness_difference > assignment.fitness_gain
		fitness_clash = demand.fitness_difference == assignment.fitness_gain
		id_superior = demand.node_id < assignment.node_id
		if fitness_upgrade or (fitness_clash and id_superior):
			self.assign(demand.component_id, demand.node_id, demand.fitness_difference)
			return

	def assign(self, component_id: int, node_id: int, fitness_difference: float):
		# TODO: One more vote for keeping components in a dictionary
		for component in self.node.get_components():
			if component.id == component_id:
				component.knowledge.assignment = AssignmentRecord(node_id, fitness_difference)

	def process_assignment(self, knowledge_packet: KnowledgePacket):
		assignment = knowledge_packet.knowledge.assignment

		if assignment.node_id != self.node.id:
			return

		# Already in ensemble, update
		# TODO: Moves between ensembles on the same node
		for instance in self.instances:
			if instance.contains(assignment.component_id):
				# TODO: Record assignment timestamps
				return

		# Process according to demand
		with self.demands[knowledge_packet.id] as demand:
			if demand.target_ensemble is EnsembleDefinition:
				# TODO: Create new instance
				print("Would create new ensemble of type " + str(demand.target_ensemble) + " with component " + assignment.component_id)
				pass
			elif demand.target_ensemble is EnsembleInstance:
				# TODO: Add knowledge to existing instance
				print("Would add  to ensemble " + str(demand.target_ensemble) + " component " + assignment.component_id)
				pass
			else:
				raise Exception("demand.target_ensemble should contain definition or instance", demand)
