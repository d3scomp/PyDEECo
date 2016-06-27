import random
import math


class Knowledge:
	pass


class Position:
	EQ_THRESHOLD = 0.000001

	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	def __str__(self):
		return str.format("[{0:f}, {1:f}]", self.x, self.y)

	def __eq__(self, other):
		return self.dist_to(other) < Position.EQ_THRESHOLD

	def __sub__(self, other):
		return Position(self.x - other.x, self.y - other.y)

	def __truediv__(self, scalar: float):
		"""Position(x1/x2, y1/y2)"""
		return Position(self.x / scalar, self.y / scalar)

	def __mul__(self, other):
		return Position(self.x * other, self.y * other)

	def __add__(self, other):
		return Position(self.x + other.x, self.y + other.y)

	def dist_to(self, other):
		return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

	def length(self):
		return math.sqrt(self.x**2 + self.y**2)


class Component:
	counter = 0
	SPEED = 0.01
	COLORS = ["red", "blue", "green"]
	random = random.Random(0)

	@staticmethod
	def genid():
		id = Component.counter
		Component.counter += 1
		return id

	def __init__(self):
		self.knowledge = Knowledge()
		self.knowledge.id = Component.genid()
		self.knowledge.position = self.gen_position()
		self.knowledge.goal = self.gen_position()
		self.knowledge.time = None
		self.knowledge.color = Component.random.choice(Component.COLORS)

		print("Component " + str(self.knowledge.id) + " created")

	def gen_position(self):
		return Position(self.random.uniform(0, 1), self.random.uniform(0, 1))

	def sim_step(self, time):
		self.knowledge.time = time

		# Run "processes"
		self.move()
		self.set_goal()
		self.status()

	def status(self):
		knowledge = self.knowledge
		print(str(knowledge.time) + " ms: " + str(knowledge.id) + " at " + str(knowledge.position) + " goal " + str(knowledge.goal) + " dist: " + str(knowledge.position.dist_to(knowledge.goal)))

	def move(self):
		if self.knowledge.position.dist_to(self.knowledge.goal) < Component.SPEED:
			self.knowledge.position = self.knowledge.goal
		else:
			vector = self.knowledge.goal - self.knowledge.position
			vector /= vector.length()
			vector *= Component.SPEED
			self.knowledge.position += vector

	def set_goal(self):
		if self.knowledge.position == self.knowledge.goal:
			self.knowledge.goal = self.gen_position()
