from random import Random

from deeco import Node
from deeco import Component
from deeco import Knowledge
from deeco import Metadata
from deeco import process

from position import Position


class Robot(Component):
	SPEED = 0.01
	COLORS = ["red", "blue", "green"]
	random = Random(0)

	def __init__(self, node: Node):
		super().__init__(node)

		self.knowledge.id = self.id
		self.knowledge.position = self.gen_position()
		self.knowledge.goal = self.gen_position()
		self.knowledge.time = None
		self.knowledge.color = self.random.choice(self.COLORS)

		print("Robot " + str(self.knowledge.id) + " created")

	def gen_position(self):
		return Position(self.random.uniform(0, 1), self.random.uniform(0, 1))

	@process
	def update_time(self, knowledge: Knowledge):
		knowledge.time = self.node.runtime.scheduler.get_time_ms()

	@process
	def status(self, knowledge):
		print(str(knowledge.time) + " ms: " + str(knowledge.id) + " at " + str(knowledge.position) + " goal " + str(
			knowledge.goal) + " dist: " + str(knowledge.position.dist_to(knowledge.goal)))

	@process
	def move(self, knowledge: Knowledge):
		if knowledge.position.dist_to(knowledge.goal) < self.SPEED:
			knowledge.position = knowledge.goal
		else:
			vector = knowledge.goal - knowledge.position
			vector /= vector.length()
			vector *= self.SPEED
			knowledge.position += vector

	@process
	def set_goal(self, knowledge: Knowledge):
		if knowledge.position == knowledge.goal:
			knowledge.goal = self.gen_position()
