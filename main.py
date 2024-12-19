import pybullet as p
import pybullet_data
import time
from box import Box
from util.calculate_force import calculate_force
from util.move_camera import move_camera
from uld import Uld

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.80665)
plane_id = p.loadURDF("plane.urdf")


p.changeDynamics(plane_id, -1, lateralFriction=0.5)


"""
uld = Uld('H1_Class_3_Instance_45_ULD_0.json')
uld_id = uld.body.render()
for item in uld.items:
    item.render()
"""

basic_box = Box()
box_id = basic_box.render()

force = calculate_force(0.5, 10, 0.05,[1,0,0])

position, orientation = p.getBasePositionAndOrientation(box_id)

basic_box.print_position()
for i in range(240*15):
    p.applyExternalForce(box_id, -1, force, position, p.WORLD_FRAME)
    move_camera(box_id)
    p.stepSimulation()
    time.sleep(1/240)

    if i % 240 == 0:
        basic_box.print_velocity()



basic_box.print_position()
basic_box.print_velocity()



p.disconnect()

