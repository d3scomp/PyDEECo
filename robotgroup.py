from core.deeco import EnsembleDefinition
from robot import Robot


class RobotGroup(EnsembleDefinition):
	def fitness(self, a: Robot.Knowledge, b: Robot.Knowledge):
		return 1 / a.position.dist_to(b.position)

	def membership(self, a: Robot, b: Robot):
		assert type(a) == Robot
		assert type(b) == Robot
		return True

	def knowledge(self, *components):
		raise "TODO: Knowledge not defined"

	def __str__(self):
		return self.__class__.__name__
