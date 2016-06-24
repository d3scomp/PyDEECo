import random
import math

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
	random = random.Random(0)

	@staticmethod
	def genid():
		id = Component.counter
		Component.counter += 1
		return id

	def __init__(self):
		self.id = Component.genid()

		self.position = self.gen_position()
		self.goal = self.gen_position()
		self.time = None

		print("Component " + str(self.id) + " created")

	def gen_position(self):
		return Position(self.random.uniform(0, 1), self.random.uniform(0, 1))

	def sim_step(self, time):
		self.time = time

		# Run "processes"
		self.move()
		self.set_goal()
		self.status()

	def status(self):
		print(str(self.time) + " ms: " + str(self.id) + " at " + str(self.position) + " goal " + str(self.goal) + " dist: " + str(self.position.dist_to(self.goal)))

	def move(self):
		if self.position.dist_to(self.goal) < Component.SPEED:
			self.position = self.goal
		else:
			vect = self.goal - self.position
			vect /= vect.length()
			vect *= Component.SPEED
			self.position += vect

	def set_goal(self):
		if self.position == self.goal:
			self.goal = self.gen_position()
