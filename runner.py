import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

from sim import Sim
from component import Component
from node import Node

print("Running simulation")

sim = Sim(snapshot_dir = "logs")

for i in range(0, 50):
	node = Node()
	node.add_component(Component())
	sim.add_node(node)

sim.run(100)
