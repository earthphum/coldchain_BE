import requests
import logging
from api_services.utils import dynamic_programming
from dotenv import load_dotenv
import os
load_dotenv()
logger = logging.getLogger(__name__)

def process_tsp(origin_coords, route, timeout=10):
    """
    Process the Traveling Salesman Problem (TSP) for a given route.

    Parameters:
        origin_coords (list/tuple): The origin coordinates [lat, lon].
        route (list): A list of coordinate pairs (each as [lat, lon]). The first and last element should be the origin.
        timeout (int, optional): Timeout for the HTTP request in seconds. Default is 10 seconds.

    Returns:
        tuple: A tuple containing:
            - ordered_route (list): The optimized route as a list of [lat, lon] (ending at the origin).
            - shortest_distance (float): The total distance of the optimized route.

    Raises:
        ValueError: If the origin coordinates or locations are invalid.
        RuntimeError: If fetching the distance matrix or TSP computation fails.
    """
    # Convert origin coordinates to floats
    try:
        origin = [float(origin_coords[0]), float(origin_coords[1])]
    except (TypeError, ValueError) as e:
        logger.error("Invalid origin coordinates: %s", origin_coords)
        raise ValueError("Invalid origin coordinates") from e

    # Ensure there are waypoints (exclude starting and ending origin if applicable)
    waypoints = route[1:-1] if len(route) >= 2 else []
    # Combine origin and waypoints into a single list for distance calculations
    locations = [origin] + waypoints
    osrm_ip = os.getenv('OSRM_IP')
    # Prepare the OSRM API URL for the cycling profile

    base_url = f"{osrm_ip}/table/v1/cycling"
    try:
        # OSRM expects coordinates in "lon,lat" format separated by semicolons
        coordinates = ";".join([f"{float(lon)},{float(lat)}" for lat, lon in locations])
    except (TypeError, ValueError) as e:
        logger.error("Invalid coordinate values in locations: %s", locations)
        raise ValueError("Invalid coordinate values") from e

    full_url = f"{base_url}/{coordinates}?annotations=distance"

    # Fetch the distance matrix from the OSRM server
    try:
        response = requests.get(full_url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error("Error fetching distance matrix from OSRM: %s", e)
        raise RuntimeError("Failed to fetch distance matrix") from e

    try:
        data = response.json()
        distance_matrix = data.get("distances")
        if distance_matrix is None:
            logger.error("No distances found in OSRM response: %s", data)
            raise RuntimeError("Distance matrix not found in response")
    except ValueError as e:
        logger.error("Error decoding JSON response: %s", e)
        raise RuntimeError("Invalid JSON response") from e

    # Compute the optimal route using TSP dynamic programming
    try:
        shortest_distance, optimal_route_indices = dynamic_programming.dp(distance_matrix=distance_matrix)
    except Exception as e:
        logger.error("Error computing TSP: %s", e)
        raise RuntimeError("Failed to compute TSP") from e

    try:
        ordered_route = [locations[i] for i in optimal_route_indices]
    except IndexError as e:
        logger.error("Optimal route indices out of range: %s", optimal_route_indices)
        raise RuntimeError("Invalid optimal route indices") from e

    # Append the origin at the end to complete the loop and return the results
    return ordered_route + [origin], shortest_distance
