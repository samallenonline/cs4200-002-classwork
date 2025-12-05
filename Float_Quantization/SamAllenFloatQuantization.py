'''

'''
import numpy as np
from pymap3d.ecef import geodetic2ecef

'''
1.2 PRECISION:
In this section, I will use latitude, longitude, and altitude
coordinates to perform some calculations. 

--Location coordinates used--
Mount Didgori, Georgia: 41.7606° N, 44.5081° E
Wat Rong Khun, Thailand: 19.8233° N, 99.7627° E

'''
'''
--Location coordinates used--
Mount Didgori, Georgia: 41.7606° N, 44.5081° E, 5334.646
Wat Rong Khun, Thailand: 19.8233° N, 99.7627° E, 1332.02
'''

# 64-BIT 
print("16-BIT")

uccs_64 = np.array([38.8936117,-104.8005516, 1965.96])
ucb_64 = np.array([40.0073943,-105.2662901, 1661.16])

# mount_didgori_64 = np.array([41.7606, 44.5081, 5334.646])
# wat_rong_64 = np.array([19.8233, 99.7627, 1332.02])

uccs_64_ecef = np.array([*geodetic2ecef(*uccs_64)])
print(uccs_64_ecef)
# array([-1270194.52877575, -4807305.93880946,  3984365.91566153])

# mount_didgori_64_ecef = np.array([*geodetic2ecef(*mount_didgori_64)])
# mount_didgori_64_ecef

ucb_64_ecef = np.array([*geodetic2ecef(*ucb_64)])
print(ucb_64_ecef)
# array([-1288472.91829674, -4720774.50988504,  4079682.41622987])

# wat_rong_64_ecef = np.array([*geodetic2ecef(*wat_rong_64)])
# wat_rong_64_ecef

print(np.linalg.norm(uccs_64_ecef - ucb_64_ecef))
# np.float64(130027.0087165725)

# np.linalg.norm(mount_didgori_64_ecef - wat_rong_64_ecef)

# 32-BIT
print("\n32-BIT")

uccs_32 = uccs_64.astype(np.float32)
ucb_32 = ucb_64.astype(np.float32)

# mount_didgori_32 = mount_didgori_64.astype(np.float32)
# wat_rong_32 = wat_rong_64.astype(np.float32)

uccs_32_ecef = np.array([*geodetic2ecef(*uccs_32)])
print(uccs_32_ecef)

# array([-1270194.4, -4807306. ,  3984366. ], dtype=float32)

# mount_didgori_32_ecef = np.array([*geodetic2ecef(*mount_didgori_32)])
#mount_didgori_32_ecef

ucb_32_ecef = np.array([*geodetic2ecef(*ucb_32)])
print(ucb_32_ecef)
# array([-1288472.6, -4720774.5,  4079682. ], dtype=float32)

# wat_rong_32_ecef = np.array([*geodetic2ecef(*wat_rong_32)])
# wat_rong_32_ecef

print(np.linalg.norm(uccs_32_ecef - ucb_32_ecef))
# np.float32(130026.67)

# np.linalg.norm(mount_didgori_32_ecef - wat_rong_32_ecef)

# 16-BIT
print("\n16-BIT")

uccs_16 = uccs_32.astype(np.float16)
ucb_16 = ucb_32.astype(np.float16)

# mount_didgori_16 = mount_didgori_64.astype(np.float16)
# wat_rong_16 = wat_rong_64.astype(np.float16)

uccs_16_ecef = np.array([*geodetic2ecef(*uccs_16)])
print(uccs_16_ecef)

# mount_didgori_16_ecef = np.array([*geodetic2ecef(*mount_didgori_16)])
# mount_didgori_16_ecef

ucb_16_ecef = np.array([*geodetic2ecef(*ucb_16)])
print(uccs_16_ecef)

# wat_rong_16_ecef = np.array([*geodetic2ecef(*wat_rong_16)])
# wat_rong_16_ecef

print(np.linalg.norm(uccs_16_ecef - ucb_16_ecef))