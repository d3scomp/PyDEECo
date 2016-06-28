import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

from sim import Sim
from deeco import Component
from deeco import Node

print("Running simulation")

sim = Sim(snapshot_dir="logs")

# Add 50 nodes hosting one component each
for i in range(0, 50):
	node = Node(sim)
	Component(node)

sim.run(100)
