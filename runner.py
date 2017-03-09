from core.deeco import Node
from core.sim import Sim
from plugins.identity_replicas import IdentityReplicas
from robot import Robot

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
