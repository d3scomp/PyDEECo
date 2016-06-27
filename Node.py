from component import Component


class Node:
	def __init__(self):
		self.components = []

	def add_component(self, component: Component):
		self.components.append(component)

	def sim_step(self, time):
		# Run components
		for component in self.components:
			component.sim_step(time)