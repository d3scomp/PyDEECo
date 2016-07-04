from random import Random

from deeco import Node
from deeco import Component
from deeco import Role
from deeco import BaseKnowledge
from deeco import process

from position import Position


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
	def __init__(self, node: Node):
		super().__init__(node)

		# Initialize knowledge
		self.knowledge.position = self.gen_position()
		self.knowledge.goal = self.gen_position()
		self.knowledge.color = self.random.choice(self.COLORS)

		print("Robot " + str(self.knowledge.id) + " created")

	# Processes follow

	@process
	def update_time(self):
		self.knowledge.time = self.node.runtime.scheduler.get_time_ms()

	@process
	def status(self):
		print(str(self.knowledge.time) + " ms: " + str(self.knowledge.id) + " at " + str(self.knowledge.position) + " goal " + str(
			self.knowledge.goal) + " dist: " + str(self.knowledge.position.dist_to(self.knowledge.goal)))

	@process
	def move(self):
		if self.knowledge.position.dist_to(self.knowledge.goal) < self.SPEED:
			self.knowledge.position = self.knowledge.goal
		else:
			vector = self.knowledge.goal - self.knowledge.position
			vector /= vector.length()
			vector *= self.SPEED
			self.knowledge.position += vector

	@process
	def set_goal(self):
		if self.knowledge.position == self.knowledge.goal:
			self.knowledge.goal = self.gen_position()
