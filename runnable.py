class Runnable:
	def run(self, scheduler):
		pass


class Runtime:
	def add_runnable(self, runnable: Runnable):
		pass

	def add_plugin(self, plugin):
		pass

	def get_scheduler(self):
		pass


class NodePlugin(Runnable):
	def __init__(self, node):
		pass


class SimPlugin(Runnable):
	def __init__(self, sim):
		super().__init__()
		self.sim = sim
		sim.add_plugin(self)

	def attach_to(self, node):
		pass
