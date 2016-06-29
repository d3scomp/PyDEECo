import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

from sim import Sim
from robot import Robot
from deeco import Node

from snapshoter import Snapshoter
from replicas import Replicas

print("Running simulation")

sim = Sim()

# add snapshoter plugin
Snapshoter(sim)

# Add X nodes hosting one component each
for i in range(0, 5):
	node = Node(sim)
	Replicas(node)
	Robot(node)

sim.run(60000)
