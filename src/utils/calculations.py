from shapely.geometry import LineString
import numpy as np

def calculate_num_buses(trip_ids):
    """
    Calculate the number of buses based on the number of unique trip IDs.

    Args:
        trip_ids (list): List of unique trip IDs.

    Returns:
        int: Number of buses.
    """
    return len(trip_ids)

def calculate_headway_min(frequencies, stop_times, trip_ids):
    """
    Calculate the average headway in minutes.

    Args:
        frequencies (pd.DataFrame): DataFrame containing frequency data.
        stop_times (pd.DataFrame): DataFrame containing stop times data.
        trip_ids (list): List of unique trip IDs.

    Returns:
        float: Average headway in minutes.
    """
    if not frequencies.empty:
        freqs_r = frequencies[frequencies["trip_id"].isin(trip_ids)]
        return freqs_r["headway_secs"].mean() / 60.0
    else:
        deps = stop_times[stop_times["trip_id"].isin(trip_ids)]
        return deps.groupby("trip_id")["dep_secs"].apply(
            lambda arr: np.diff(np.sort(arr)).mean() / 60
        ).mean()

def calculate_avg_speed(shapes_grouped, stop_times, trips_r):
    """
    Calculate the average speed of a route.

    Args:
        shapes_grouped (pd.DataFrameGroupBy): Grouped DataFrame of shapes.
        stop_times (pd.DataFrame): DataFrame containing stop times data.
        trips_r (pd.DataFrame): DataFrame containing trips data for a specific route.

    Returns:
        float: Average speed in the route.
    """
    avg_speeds = []
    for sid in trips_r["shape_id"].dropna().unique():
        pts = shapes_grouped.get_group(sid).values
        pts_float = [
            [float(coord.replace(",", ".")) if isinstance(coord, str) else float(coord) for coord in pt]
            for pt in pts
        ]
        line = LineString(pts_float)
        duration = stop_times[
            stop_times["trip_id"].isin(trips_r[trips_r["shape_id"] == sid]["trip_id"])
        ].agg({"arr_secs": "max", "dep_secs": "min"})
        travel_time = duration["arr_secs"] - duration["dep_secs"]
        if travel_time > 0:
            avg_speeds.append((line.length) / (travel_time / 3600))
    return np.mean(avg_speeds) if avg_speeds else None

def calculate_demand_est(stop_times, trip_ids):
    """
    Estimate the demand proxy based on stop times.

    Args:
        stop_times (pd.DataFrame): DataFrame containing stop times data.
        trip_ids (list): List of unique trip IDs.

    Returns:
        float: Estimated demand proxy.
    """
    return stop_times[stop_times["trip_id"].isin(trip_ids)] \
        .groupby("stop_id").size().mean()