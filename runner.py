import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

from sim import Sim
from robot import Robot
from deeco import Node

from snapshoter import Snapshoter
from identity_replicas import IdentityReplicas

print("Running simulation")

sim = Sim()

# Add snapshoter plugin
#Snapshoter(sim)

# Add identity replicas plugin (provides replicas using deep copies of original knowledge)
IdentityReplicas(sim)

# Add X nodes hosting one component each
for i in range(0, 5):
	node = Node(sim)
	robot = Robot()
	node.add_component(robot)

# Run the simulation
sim.run(60000)
