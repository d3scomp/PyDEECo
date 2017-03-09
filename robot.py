from random import Random

from core.deeco import BaseKnowledge
from core.deeco import Component
from core.deeco import Node
from core.deeco import Role
from core.deeco import process
from core.position import Position


# Role
class Rover(Role):
	def __init__(self):
		super().__init__()
		self.position = None
		self.goal = None


# Component
class Robot(Component):
	SPEED = 0.01
	COLORS = ["red", "blue", "green"]
	random = Random(0)

	@staticmethod
	def gen_position():
		return Position(Robot.random.uniform(0, 1), Robot.random.uniform(0, 1))

	# Knowledge definition
	class Knowledge(BaseKnowledge, Rover):
		def __init__(self):
			super().__init__()
			self.color = None

	# Component initialization
	def __init__(self):
		super().__init__()

		# Initialize knowledge
		self.knowledge.position = self.gen_position()
		self.knowledge.goal = self.gen_position()
		self.knowledge.color = self.random.choice(self.COLORS)

		print("Robot " + str(self.knowledge.id) + " created")

	# Processes follow

	@process(period_ms=1000)
	def update_time(self, node: Node):
		self.knowledge.time = node.runtime.scheduler.get_time_ms()

	@process(period_ms=1000)
	def status(self, node: Node):
		print(str(self.knowledge.time) + " ms: " + str(self.knowledge.id) + " at " + str(self.knowledge.position) + " goal " + str(
			self.knowledge.goal) + " dist: " + str(self.knowledge.position.dist_to(self.knowledge.goal)))

	@process(period_ms=1000)
	def move(self, node: Node):
		if self.knowledge.position.dist_to(self.knowledge.goal) < self.SPEED:
			self.knowledge.position = self.knowledge.goal
		else:
			vector = self.knowledge.goal - self.knowledge.position
			vector /= vector.length()
			vector *= self.SPEED
			self.knowledge.position += vector

	@process(period_ms=1000)
	def set_goal(self, node: Node):
		if self.knowledge.position == self.knowledge.goal:
			self.knowledge.goal = self.gen_position()
