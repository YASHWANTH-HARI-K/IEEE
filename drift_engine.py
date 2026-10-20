import numpy as np

def predict_debris_drift(start_lat, start_long, current_u=0.45, current_v=0.20, wind_u=5.2, wind_v=3.1, hours=48, alpha=0.03):
    """
    Calculates future coordinates using 2D Lagrangian particle tracking with USCG Leeway Model.
    
    :param start_lat: Initial Latitude from YOLOv8 detection centroid
    :param start_long: Initial Longitude from YOLOv8 detection centroid
    :param current_u: Ocean current Eastward velocity (m/s)
    :param current_v: Ocean current Northward velocity (m/s)
    :param wind_u: Surface wind Eastward velocity (m/s)
    :param wind_v: Surface wind Northward velocity (m/s)
    :param hours: Projection time window
    :param alpha: Windage leeway transfer factor (~3% for floating net structures)
    :return: Tuple of (24h_lat, 24h_long, 48h_lat, 48h_long)
    """
    # Net velocity vector calculation
    net_u = current_u + (alpha * wind_u)
    net_v = current_v + (alpha * wind_v)
    
    R_earth = 6378137.0  # Earth radius in meters
    
    # 24-Hour Projection
    sec_24 = 24 * 3600
    dx_24, dy_24 = net_u * sec_24, net_v * sec_24
    dlat_24 = (dy_24 / R_earth) * (180 / np.pi)
    dlong_24 = (dx_24 / (R_earth * np.cos(np.pi * start_lat / 180))) * (180 / np.pi)
    
    # 48-Hour Projection
    sec_48 = 48 * 3600
    dx_48, dy_48 = net_u * sec_48, net_v * sec_48
    dlat_48 = (dy_48 / R_earth) * (180 / np.pi)
    dlong_48 = (dx_48 / (R_earth * np.cos(np.pi * start_lat / 180))) * (180 / np.pi)
    
    return (
        start_lat + dlat_24, start_long + dlong_24,
        start_lat + dlat_48, start_long + dlong_48
    )