from core.deeco import Node
from core.sim import Sim
from core.position import Position
from plugins.identity_replicas import IdentityReplicas
from plugins.simplenetwork import SimpleNetwork
from plugins.walker import Walker
from robot import Robot

print("Running simulation")

sim = Sim()

# Add snapshoter plugin
#Snapshoter(sim)

# Add identity replicas plugin (provides replicas using deep copies of original knowledge)
IdentityReplicas(sim)

# Add simple network device
SimpleNetwork(sim)

# Add X nodes hosting one component each
for i in range(0, 5):
	position = Position(2 * i, 3 * i)

	node = Node(sim)
	Walker(node, position)

	robot = Robot(node)

	node.add_component(robot)

# Run the simulation
sim.run(60000)
