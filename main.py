import pybullet as p
import pybullet_data
import time
from typing import Final

from box import Box
from util.calculate_force import calculate_force_and_acceleration
from util.move_camera import move_camera
from uld import Uld

FRICTION: Final = 0.3

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.80665)
plane_id = p.loadURDF("plane.urdf")

p.changeDynamics(plane_id, -1, lateralFriction=FRICTION)


"""
uld = Uld('H1_Class_3_Instance_45_ULD_0.json')
uld_id = uld.body.render()
for item in uld.items:
    item.render()
"""

basic_box = Box()
box_id = basic_box.render()

position, orientation = p.getBasePositionAndOrientation(box_id)
basic_box.print_position()

for i in range(240*15):
    force, _ = calculate_force_and_acceleration(FRICTION, 10,[1,0,0], int(i/240), 3, 2)
    p.applyExternalForce(box_id, -1, force, position, p.WORLD_FRAME)
    move_camera(box_id)
    p.stepSimulation()
    time.sleep(1/240)

    if i % 240 == 0:
        basic_box.print_velocity()

basic_box.print_position()
basic_box.print_velocity()

p.disconnect()

