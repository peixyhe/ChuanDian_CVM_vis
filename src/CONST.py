'''
    define some constants
'''
import math

## geographic region:
##                                         up(-90.0, 90.0)
##                    left(-180.0, 180.0)                     right(-180.0, 180.0)
##                                         down(-90.0, 90.0)

up = 33.4      
down = 21.8
left = 97.8   
right = 107

scale = 10
min_mag = 1



ANGLE2KILOMETERS = (  2 * math.pi * 6371.393  / 360.0 / scale  ) * math.sqrt(    1 + (  math.cos( math.radians( (up + down) / 2.0 ) )  ) ** 2.0    ) / (2.0 ** 0.5)        # EARTH_RADIUS = 6371393.0(m)
ANGLE2METERS     = (  2 * math.pi * 6371393.0 / 360.0 / scale  ) * math.sqrt(    1 + (  math.cos( math.radians( (up + down) / 2.0 ) )  ) ** 2.0    ) / (2.0 ** 0.5)

print(ANGLE2KILOMETERS)
print(1.0 / ANGLE2KILOMETERS)
print(ANGLE2METERS)
