from core.deeco import EnsembleDefinition
from robot import Robot

class RobotGroup(EnsembleDefinition):
	def fitness(self, *components):
		pass

	def membership(self, a: Robot, b: Robot):
		assert type(a) == Robot
		assert type(b) == Robot
		return True

	def knowledge(self, *components):
		pass
