import jsonpickle as json
import os
import types
from queue import PriorityQueue

from runnable import Runnable


class Timer:
	pass


class Scheduler:
	def run(self):
		pass

	def schedule_timer(self, timer: Timer):
		pass

	def get_time_ms(self):
		pass

	def set_timer(self, method: types.MethodType, time_ms: int):
		self.schedule_timer(Timer(self, method, time_ms))

	def set_periodic_timer(self, method: types.MethodType, period_ms: int, time_ms: int = 0):
		self.schedule_timer(PeriodicTimer(self, method, period_ms, time_ms))


class SimScheduler(Scheduler):
	def __init__(self):
		self.events = PriorityQueue()
		self.time_ms = None

	def run(self, limit_ms: int):
		self.time_ms = 0
		while not self.events.empty() and self.time_ms < limit_ms:
			event = self.events.get()
			self.time_ms = event.time_ms
			event.run(self.time_ms)

	def schedule_timer(self, timer: Timer):
		self.events.put(timer)

	def get_time_ms(self):
		return self.time_ms


class Timer:
	def default_method(self, time_ms):
		print("No method set for " + str(type(self)) + " at " + str(time_ms))

	def __init__(self, scheduler: Scheduler, method: types.MethodType, time_ms):
		self.scheduler = scheduler
		self.time_ms = time_ms
		self.method = method

	def __lt__(self, other):
		return self.time_ms < other.time_ms

	def run(self, time_ms: int):
		self.method(time_ms)


class PeriodicTimer(Timer):
	def __init__(self, scheduler: Scheduler, method: types.MethodType, period_ms: int, time_ms: int):
		super().__init__(scheduler, method, time_ms)
		self.period_ms = period_ms

	def run(self, time_ms: int):
		super().run(time_ms)
		self.time_ms += self.period_ms
		self.scheduler.schedule_timer(self)


class Sim:
	def __init__(self, snapshot_dir=None):
		self.scheduler = SimScheduler()

		self.runnables = []
		self.snapshot_dir = snapshot_dir
		self.time = 0

		if snapshot_dir is not None:
			try:
				os.mkdir(self.snapshot_dir)
			except FileExistsError as e:
				pass

	def add_runnable(self, runnable: Runnable):
		self.runnables.append(runnable)

	def run(self, limit_ms: int):
		# Schedule runnable in the system nodes
		for node in self.runnables:
			node.run(self.scheduler)

		# Schedule snapshot execution
		self.scheduler.set_periodic_timer(self.snapshot_system, period_ms=1000)

		self.scheduler.run(limit_ms)

		print("All done")

	def snapshot_system(self, time_ms: int):
			# Snapshot the system
			if self.snapshot_dir is not None:
				log = open(self.snapshot_dir + os.sep + str(time_ms) + ".json", "w")
				dump = json.encode(self)
				log.write(dump)
				log.close()
