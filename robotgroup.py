from abc import abstractmethod

from core.deeco import EnsembleDefinition, BaseKnowledge
from core.deeco import Role
from core.position import Position
from robot import Robot


# Role
class Group(Role):
	def __init__(self):
		super().__init__()
		self.center = None
		self.members = []


class RobotGroup(EnsembleDefinition):
	class Knowledge(BaseKnowledge, Group):
		def __init__(self):
			super().__init__()

	def fitness(self, a: Robot.Knowledge, b: Robot.Knowledge):
		return 1 / a.position.dist_to(b.position)

	def membership(self, a: Robot, b: Robot):
		assert type(a) == Robot
		assert type(b) == Robot
		return True

	def knowledge(self, a: Robot.Knowledge, b: Robot.Knowledge):
		knowledge = self.Knowledge()
		knowledge.center = Position.average(a.position, b.position)
		knowledge.members = [a, b]

		return knowledge

	def __str__(self):
		return self.__class__.__name__
