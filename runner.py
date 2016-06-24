import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

from sim import Sim
from component import Component

print("Hello world")

c0 = Component()
c1 = Component()
c2 = Component()

sim = Sim(snapshot_dir = "logs")
sim.addcomponent(c0)
sim.addcomponent(c1)
sim.addcomponent(c2)

sim.run(100)
