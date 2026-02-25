

from models.Camera import Camera
from models.Detector import Detector
from tracking.System import System

camera = Camera(0)
detector = Detector(camera, None)
system = System(detector)
system.start()

camera.finalize()


