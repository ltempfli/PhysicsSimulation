import pybullet as p
import pybullet_data
import time

from uld import Uld


p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
plane_id = p.loadURDF("plane.urdf")

uld = Uld('H1_Class_3_Instance_45_ULD_0.json')
uld.body.render()
for item in uld.items:
    item.render()

# position = [0, 0, 0.5]
# force = [80, 0, 0]  # Force to apply to the car to simulate acceleration
for _ in range(10000):
    #p.applyExternalForce(big_box, -1, force, position, p.WORLD_FRAME)
    #move_camera(big_box)
    p.stepSimulation()
    time.sleep(1/240)

p.disconnect()

