import math
from wpimath.geometry import Rotation2d

def getTicksFromRotation( rotation:Rotation2d, ticksPerRotation:float ) -> int:
    radians:float = rotation.radians() # type: ignore
    ticks:int = int( radians * ticksPerRotation / ( 2 * math.pi ) )
    return ticks

def getRotationFromTicks( ticks:float, ticksPerRotation:float ) -> Rotation2d:
    radians:float = ticks * ( 2 * math.pi ) / ticksPerRotation
    rotation = Rotation2d( value=radians )
    return rotation

def getVelocityTp100msToMps( ticksPer100ms:float, ticksPerRotation:float, radius:float ) -> float:
    ticksPerSec:float = ticksPer100ms * 10
    rotationsPerSec:float = ticksPerSec / ticksPerRotation
    metersPerSec:float = rotationsPerSec * ( 2 * math.pi * radius )
    return metersPerSec

def getVelocityMpsToTp100ms( metersPerSec:float, ticksPerRotation:float, radius:float ) -> float:
    rotationsPerSec:float = metersPerSec / ( 2 * math.pi * radius )
    ticksPerSec:float = rotationsPerSec * ticksPerRotation
    ticksPer100ms:float = ticksPerSec / 10
    return ticksPer100ms

def getDistanceTicksToMeters( ticks:float, ticksPerRotation:float, radius:float ) -> float:
    rotations:float = ticks / ticksPerRotation
    meters:float = rotations * ( 2 * math.pi * radius )
    return meters


def getDistanceMetersToTicks( meters:float, ticksPerRotation:float, radius:float ) -> float:
    rotations:float = meters / ( 2 * math.pi * radius )
    ticks:float = rotations * ticksPerRotation
    return ticks