from wpimath.geometry import *
from wpimath.kinematics import *
from pyfrc.physics.core import PhysicsInterface

from ctre import *
from ctre.sensors import *

from subsystems.swervedrive import SwerveDrive4

class PhysicsEngine:
    def __init__(self,physics_controller,robot):
        self.physics_controller:PhysicsInterface = physics_controller
        self.drivetrain:SwerveDrive4 = robot.subsystems[0]
        self.gyroSim:BasePigeonSimCollection = self.drivetrain.gyro.getSimCollection()

    def update_sim(self, now, tm_diff):
        if self.drivetrain is None:
            return
        elif self.drivetrain.cSpeeds is None:
            return
        
        # Physics Controller Drivetrain Simulation
        cSpeeds:ChassisSpeeds = self.drivetrain.cSpeeds
        newPose:Pose2d = self.physics_controller.drive( cSpeeds, tm_diff )

        # Gyro Simulation
        newRot:Rotation2d = newPose.rotation()
        self.gyroSim.setRawHeading( newRot.degrees() )