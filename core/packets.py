from enum import Enum
from copy import deepcopy


class PacketType(Enum):
	RAW = 0
	KNOWLEDGE = 1
	TEXT = 2
	DEMAND = 3


class Packet:
	def __init__(self):
		self.type = PacketType.RAW

	def __init__(self, type: PacketType):
		self.type = type


class KnowledgePacket(Packet):
	def __init__(self, component, time_ms: int):
		super().__init__(PacketType.KNOWLEDGE)
		self.id = component.id
		self.timestamp_ms = time_ms
		self.knowledge = deepcopy(component.knowledge)


class TextPacket(Packet):
	def __init__(self, text: str):
		super().__init__(PacketType.TEXT)
		self.text = text

	def __str__(self):
		return self.text


class DemandPacket(Packet):
	def __init__(self, demanded_component_id: int, demanding_node_id: int):
		super().__init__(PacketType.DEMAND)
		self.demanded_id = demanded_component_id
		self.demanding_id = demanding_node_id

	def __str__(self):
		return "[node " + str(self.demanding_id) + " wants component " + str(self.demanded_id) + "]"
