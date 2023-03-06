import time
from wpilib import TimedRobot, run
from ntcore import NetworkTableInstance, Event, EventFlags

from build import Build

from subsystems import Subsystems
from subsystems.swervedrive import SwerveDrive4
#from subsystems.pneumatics import RobotCompressor
#from subsystems.arm import Arm
#from subsystems.claw import Claw
#from subsystems.bumper import Bumper
#from subsystems.limelight import Limelight

class Robot(TimedRobot):
    def robotInit(self): 
        # Initialization Wait for Canbus (Known Issue)
        time.sleep(2)

        # Get Build Settings
        Build().buildInitConfig()
        Build().buildVariables()

        # Build Subsystems
        self.subsystems = []

        # Add SwerveDrive to Subsystems
        try:
            self.subsystems.append( SwerveDrive4() )
        except:
            pass

        # Add RobotCompressor to Subsystems
        try:
            self.subsystems.append( RobotCompressor() )
        except:
            pass

        # Add Arm to Subsystems
        try:
            self.subsystems.append( Arm() )
        except:
            pass

        # Add Claw to Subsystems
        try:
            self.subsystems.append( Claw() )
        except:
            pass

        # Add Bumper to Subsystems
        try:
            self.subsystems.append( Bumper() )
        except:
            pass

        # Add Limelight to Subsystems
        try:
            self.subsystems.append( Limelight() )
        except:
            pass

        # Load NT Table for Testing
        self.ntInst = NetworkTableInstance.getDefault()
        ntTest = self.ntInst.getTable( ".Testing" )
        ntTestVars = ntTest.getTopics()
        for i in range(len(ntTestVars)):
            vName = ntTestVars[i].getName().removeprefix("/.Testing/") 
            vValue = ntTest.getBoolean( vName, False )
            exec(f"self.test_{vName} = {vValue}")
        self.startNtListener()

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
    def testPeriodic(self):
        for i in range(len(self.subsystems)):
            s:Subsystems = self.subsystems[i]
            sName = s.__class__.__name__
            try:
                runInTest = eval( f"self.test_{sName}" )
            except:
                runInTest = False
            
            if runInTest:
                s.run()
    def testExit(self): pass

    def disabledInit(self): pass
    def disabledPeriodic(self): pass
    def disabledExit(self): pass

    def startNtListener(self):
        self.ntInst.addListener(
            [ "/.Testing" ],
            EventFlags.kValueAll,
            self.updateNtTestValues
        )
    def updateNtTestValues(self, event:Event):
        # Get Variable Name and New Value
        varName = event.data.topic.getName().removeprefix(f"/.Testing/")
        newValue = event.data.value.value()
        # Set Variable
        exec( f"self.test_{varName} = {newValue}" )


if __name__ == '__main__':
    run(Robot)