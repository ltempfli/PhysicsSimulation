import pybullet as p
import pybullet_data
import time
from typing import Final

from util.calculate_force import calculate_force_and_acceleration
from util.move_camera import move_camera
from uld import Uld

FRICTION: Final = 0.3

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.80665)
plane_id = p.loadURDF("plane.urdf")

p.changeDynamics(plane_id, -1, lateralFriction=FRICTION)

uld = Uld('H1_Class_3_Instance_45_ULD_0.json', scaling_factor=0.02)
uld_id = uld.body.render()
for item in uld.items:
    item.render()

position, orientation = p.getBasePositionAndOrientation(uld_id)

for i in range(240*15):
    # wait one second before force is applied
    if int(i/240) >= 1:
        force, _ = calculate_force_and_acceleration(FRICTION, uld.body.mass, [1, 0, 0], int((i-240) / 240), 4, 2)
        p.applyExternalForce(uld_id, -1, force, position, p.WORLD_FRAME)
    move_camera(uld_id)
    p.stepSimulation()
    time.sleep(1/240)

p.disconnect()