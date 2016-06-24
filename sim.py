from component import Component

class Sim:
	def __init__(self):
		self.components = []

	def addcomponent(self, component: Component):
		self.components.append(component)

	def run(self, limit: int):
		for time in range(0, limit):
			print("Sim at " + str(time) + " ms")
			for component in self.components:
				component.sim_step(time)