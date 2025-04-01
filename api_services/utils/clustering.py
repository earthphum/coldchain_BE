import logging
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)

def cluster(customer_latlng_list, origin_latlng, n_clusters):
    """
    Cluster customer locations into groups and generate a route for each cluster.
    
    Parameters:
        customer_latlng_list (list): A list of customer coordinates in the format [[lat, lon], ...].
        origin_latlng (list or tuple): The origin coordinates as [lat, lon].
        n_clusters (int): The number of clusters (usually equal to the number of riders).
    
    Returns:
        list: A list of routes, where each route is a list of coordinates starting and ending at the origin.
    
    Raises:
        ValueError: If the number of clusters exceeds the number of customers, or if input coordinates are invalid.
    """
    # Validate input: number of clusters should not exceed the number of customer locations.
    if not customer_latlng_list or len(customer_latlng_list) < n_clusters:
        raise ValueError("Number of clusters cannot exceed number of customers.")
    
    # Convert origin coordinates to floats.
    try:
        origin = [float(coord) for coord in origin_latlng]
    except (ValueError, TypeError) as e:
        logger.error("Invalid origin coordinates: %s", origin_latlng)
        raise ValueError("Invalid origin coordinates.") from e

    # Convert customer coordinates to floats.
    try:
        customer_points = [list(map(float, latlng)) for latlng in customer_latlng_list]
    except (ValueError, TypeError) as e:
        logger.error("Invalid customer coordinates in list: %s", customer_latlng_list)
        raise ValueError("Invalid customer coordinates in list.") from e

    # Initialize KMeans with production-tuned parameters.
    kmeans = KMeans(
        n_clusters=n_clusters,
        init='k-means++',
        n_init=100,
        max_iter=1000,
        random_state=42
    )
    kmeans.fit(customer_points)
    clusters = kmeans.labels_

    routes = []
    # Generate a route for each cluster.
    for i in range(n_clusters):
        cluster_points = [
            customer_points[j] for j in range(len(customer_points))
            if clusters[j] == i
        ]
        route = create_route(cluster_points, origin)
        routes.append(route)

    return routes


def create_route(cluster_points, origin):
    """
    Create a route that starts and ends at the origin and passes through all points in the cluster.
    
    Parameters:
        cluster_points (list): A list of coordinates (each in [lat, lon] format) for a cluster.
        origin (list): The origin coordinates as [lat, lon].
    
    Returns:
        list: A list of coordinates representing the route.
    """
    # Prepend the origin to the list and append the origin at the end to complete the loop.
    return [origin] + cluster_points + [origin]
