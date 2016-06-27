import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

from sim import Sim
from component import Component

print("Hello world")

sim = Sim(snapshot_dir = "logs")

for i in range(0, 50):
	sim.addcomponent(Component())

sim.run(100)
