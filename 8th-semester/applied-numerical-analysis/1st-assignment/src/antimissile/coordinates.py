"""Geographic coordinate utilities for the anti-missile simulation.

Converts geodetic coordinates (latitude, longitude, elevation) to a local
East-North-Up (ENU) Cartesian frame centred at the radar station, using a
flat-Earth approximation valid within the ~30 km operational radius.
"""

import numpy as np

# ── Reference point: radar station ────────────────────────────────────────────
RADAR_GEO = (40.5955016, 23.1053063, 1021.6)  # (lat °, lon °, elev m ASL)

_R_EARTH      = 6_371_000.0                    # mean Earth radius [m]
_LAT_REF_RAD  = np.radians(RADAR_GEO[0])


def geo_to_enu(lat: float, lon: float, elev: float) -> np.ndarray:
    """Convert geodetic coordinates to local ENU in metres.

    The ENU frame origin is the radar station.  The *Up* axis points away
    from the Earth's surface; the *North* and *East* axes are tangent to the
    surface at the reference point.

    Args:
        lat:  Geodetic latitude in decimal degrees.
        lon:  Geodetic longitude in decimal degrees.
        elev: Elevation above mean sea level in metres.

    Returns:
        3-element NumPy array ``[east, north, up]`` in metres.
    """
    dlat  = np.radians(lat - RADAR_GEO[0])
    dlon  = np.radians(lon - RADAR_GEO[1])
    north = dlat * _R_EARTH
    east  = dlon * _R_EARTH * np.cos(_LAT_REF_RAD)
    up    = elev - RADAR_GEO[2]
    return np.array([east, north, up], dtype=float)


# ── Ground level in ENU ────────────────────────────────────────────────────────
# Sea level (0 m ASL) corresponds to ENU z = -radar_elevation
GROUND_Z_ENU: float = -RADAR_GEO[2]   # ≈ -1021.6 m
