import pybullet as p

def move_camera(box_id: int, camera_distance: int= 5)-> None:

    position, orientation = p.getBasePositionAndOrientation(box_id)

    # Calculate the new camera position based on the object's position and offset
    #camera_pos = [position[0] + camera_offset[0], position[1] + camera_offset[1], position[2] + camera_offset[2]]

    # Update the camera to smoothly follow the object
    p.resetDebugVisualizerCamera(camera_distance, -30, -45, position)