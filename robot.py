from wpilib import TimedRobot, run
from ntcore import NetworkTableInstance

from build import Build

from subsystems import Subsystems
from subsystems.swervedrive import SwerveDrive4
from subsystems.pneumatics import RobotCompressor
from subsystems.arm import Arm
from subsystems.claw import Claw
from subsystems.bumper import Bumper
from subsystems.limelight import Limelight

class Robot(TimedRobot):
    def robotInit(self): 
        # Get Build Settings
        Build().buildInitConfig()
        Build().buildVariables()

        # Build Subsystems
        self.subsystems = [
            SwerveDrive4(),
            #RobotCompressor(),
            #Arm(),
            #Claw(),
            #Bumper(),
            #Limelight(),
        ]

    def robotPeriodic(self): pass

    def autonomousInit(self): pass
    def autonomousPeriodic(self): pass
    def autonomousExit(self): pass
 
    def teleopInit(self): pass
    def teleopPeriodic(self):
        for i in range(len(self.subsystems)):
            s:Subsystems = self.subsystems[i]
            s.run()
    def teleopExit(self): pass

    def testInit(self): pass
    def testPeriodic(self): pass
    def testExit(self): pass

    def disabledInit(self): pass
    def disabledPeriodic(self): pass
    def disabledExit(self): pass

if __name__ == '__main__':
    run(Robot)