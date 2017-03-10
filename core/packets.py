from enum import Enum
from copy import deepcopy

from core.deeco import Component


class PacketType(Enum):
	RAW = 0
	KNOWLEDGE = 1


class Packet:
	def __init__(self):
		self.type = PacketType.RAW


class KnowledgePacket(Packet):
	def __init__(self, component: Component):
		self.type = PacketType.KNOWLEDGE
		self.knowledge = deepcopy(component.knowledge)
