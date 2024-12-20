import pybullet as p
import pybullet_data
import time
from typing import Final

from physic_engine.calculate_force import calculate_force_and_acceleration
from physic_engine.move_camera import move_camera
from model.uld import Uld

ITEM_FRICTION: Final = 0.3
ULD_FRICTION: Final = 0.5
GROUND_FRICTION: Final = 0.8


p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.80665)
plane_id = p.loadURDF("plane.urdf")

p.changeDynamics(plane_id, -1, lateralFriction=GROUND_FRICTION)

uld = Uld('data/uld_loading_patterns/H1_Class_3_Instance_45_ULD_0.json', scaling_factor=0.02, uld_friction=ITEM_FRICTION, item_friction=ITEM_FRICTION)
uld_id = uld.body.render()
for item in uld.items:
    item.render()

position, _ = p.getBasePositionAndOrientation(uld_id)

for i in range(240*10):
    # wait one second before force is applied
    if int(i/240) >= 1:
        force, _ = calculate_force_and_acceleration(ITEM_FRICTION, uld.body.mass, [1, 0, 0], int((i - 240) / 240), 7, 2)
        p.applyExternalForce(uld_id, -1, force, position, p.WORLD_FRAME)
    move_camera(uld_id)
    p.stepSimulation()
    time.sleep(1/240)

nfb, nfb_rel = uld.evaluate_nfb()
print("---------------------------------------------------------------------")
print("NFB: " + str(nfb) + " out of " + str(len(uld.items)))
print("NFB (relative): " + str(nfb_rel))
print("---------------------------------------------------------------------")

p.disconnect()