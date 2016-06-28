import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

from sim import Sim
from robot import Robot
from deeco import Node

print("Running simulation")

sim = Sim(snapshot_dir="logs")

# Add X nodes hosting one component each
for i in range(0, 5):
	node = Node(sim)
	Robot(node)

sim.run(60000)
