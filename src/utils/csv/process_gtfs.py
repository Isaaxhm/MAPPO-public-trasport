# Refactored script to make it modular and reusable for processing GTFS data.
import os
import pandas as pd
from shapely.geometry import LineString, Point
from shapely.ops import unary_union
import numpy as np
from utils.calculations import calculate_num_buses, calculate_headway_min, calculate_avg_speed, calculate_demand_est


def load_gtfs_data(gtfs_dir):
    """
    Load GTFS data from the specified directory.

    Args:
        gtfs_dir (str): Path to the GTFS directory.

    Returns:
        dict: A dictionary containing loaded GTFS data as pandas DataFrames.
    """
    data = {
        "routes": pd.read_csv(os.path.join(gtfs_dir, "routes.txt")),
        "trips": pd.read_csv(os.path.join(gtfs_dir, "trips.txt")),
        "stop_times": pd.read_csv(os.path.join(gtfs_dir, "stop_times.txt")),
        "stops": pd.read_csv(os.path.join(gtfs_dir, "stops.txt")),
        "frequencies": pd.read_csv(os.path.join(gtfs_dir, "frequencies.txt")),
        "shapes": pd.read_csv(os.path.join(gtfs_dir, "shapes.txt"))
    }
    return data

def time_to_seconds(t):
    """
    Convert time in HH:MM:SS format to seconds.

    Args:
        t (str): Time in HH:MM:SS format.

    Returns:
        int: Time in seconds.
    """
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s

def process_routes(data):
    """
    Process GTFS data to generate route summaries.

    Args:
        data (dict): Dictionary containing GTFS data as pandas DataFrames.
        output_dir (str): Directory to save the route summaries.

    Returns:
        pd.DataFrame: A DataFrame containing route summaries.
    """
    routes = data["routes"]
    trips = data["trips"]
    stop_times = data["stop_times"]
    stops = data["stops"]
    frequencies = data["frequencies"]
    shapes = data["shapes"]
    n = 0

    stop_times = stop_times.merge(
        stops[["stop_id", "stop_lat", "stop_lon"]],
        on="stop_id",
        how="left"
    )

    stop_times["dep_secs"] = stop_times["departure_time"].apply(time_to_seconds)
    stop_times["arr_secs"] = stop_times["arrival_time"].apply(time_to_seconds)

    route_summaries = []
    shapes_grouped = shapes.groupby("shape_id")[["shape_pt_lon", "shape_pt_lat"]]

    for route_id in routes["route_id"].unique():
        trips_r = trips[trips["route_id"] == route_id]
        trip_ids = trips_r["trip_id"].unique()

        num_buses = calculate_num_buses(trip_ids)
        headway_min = calculate_headway_min(frequencies, stop_times, trip_ids)
        avg_speed = calculate_avg_speed(shapes_grouped, stop_times, trips_r)
        demand_est = calculate_demand_est(stop_times, trip_ids)

        pts = [
            Point((lat),(lon))
            for lat, lon in stop_times[stop_times["trip_id"].isin(trip_ids)][["stop_lat", "stop_lon"]].values
        ]

        # Compute coverage area only if there are at least 3 valid points
        valid_pts = [p for p in pts if p.is_valid]
        if len(valid_pts) >= 3:
            hull = unary_union(valid_pts).convex_hull
            coverage_area = hull.area
        else:
            coverage_area = None

        # Write route summary to a text file
        with open(os.path.join("data/route_summaries.txt"), "a") as f:
            f.write(f"Route {route_id}: buses={num_buses}, headway={headway_min:.2f}min, "
                    f"speed={avg_speed:.2f}, coverage={coverage_area:.2f}, demand={demand_est:.2f}\n")

        n += 1

        # Append route summary to the list
        route_summaries.append({
            "route_id": route_id,
            "num_buses": num_buses,
            "headway_min": headway_min,
            "avg_speed": avg_speed,
            "coverage_area": coverage_area,
            "demand_est": demand_est
        })

    return pd.DataFrame(route_summaries)

def save_route_summaries(df, output_dir):
    """
    Save route summaries to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame containing route summaries.
        output_dir (str): Directory to save the output file.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define the output file path
    output_path = os.path.join(output_dir, "route_attributes.csv")

    # Save the DataFrame to a CSV file
    df.to_csv(output_path, index=False)

    # Print a success message
    print(f"Route summaries saved to {output_path}")

