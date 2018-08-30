from core.deeco import Node
from core.sim import Sim
from core.position import Position
from plugins.identity_replicas import IdentityReplicas
from plugins.simplenetwork import SimpleNetwork
from plugins.walker import Walker
from plugins.knowledgepublisher import KnowledgePublisher
from plugins.ensemblereactor import EnsembleReactor

from robot import Robot
from robotgroup import RobotGroup
from plugins.snapshoter import Snapshoter

print("Running simulation")

sim = Sim()

# Add snapshoter plugin
Snapshoter(sim)

# Add identity replicas plugin (provides replicas using deep copies of original knowledge)
IdentityReplicas(sim)

# Add simple network device
SimpleNetwork(sim, range_m=3, delay_ms_mu=20, delay_ms_sigma=5)

# Add X nodes hosting one component each
for i in range(0, 5):
	position = Position(2 * i, 3 * i)

	node = Node(sim)
	Walker(node, position)
	KnowledgePublisher(node)
	EnsembleReactor(node, [RobotGroup()])

	robot = Robot(node)

	node.add_component(robot)

# Run the simulation
sim.run(60000)
