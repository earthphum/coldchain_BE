import logging
import hashlib
import json
from datetime import datetime
from ..models import RiderHistoryData, OrdersData, OriginData, CustomersData, RoutePlanCache
from ..utils import traveling_salesman_problem, clustering

logger = logging.getLogger(__name__)

def _generate_cache_key(delivery_date, rider_names, orders_queryset):
    """
    Generate a unique cache key based on:
      - delivery_date: The delivery date
      - rider_names: A sorted list of rider names
      - orders: A sorted list of order IDs for that date
    """
    order_ids = list(orders_queryset.values_list('id', flat=True))
    key_data = {
        "delivery_date": delivery_date,
        "rider_names": sorted(rider_names),
        "orders": sorted(order_ids)
    }
    key_string = json.dumps(key_data, sort_keys=True)
    return hashlib.sha256(key_string.encode()).hexdigest()

def plan_routes(num_riders, delivery_date, rider_names):
    """
    Plan delivery routes based on the given input parameters.
    Uses caching if delivery_date, rider names, and orders haven't changed.

    Parameters:
        num_riders (int): Number of riders.
        delivery_date (str): Delivery date in YYYY-MM-DD format.
        rider_names (list): List of rider names.

    Returns:
        dict: Contains delivery details, coordinates, clusters, and assigned routes.
    """
    # Validate that the number of rider names matches the given number of riders
    if len(rider_names) != num_riders:
        raise ValueError("The number of rider names must match num_riders.")

    # Fetch delivery orders for the specified date
    deliveries = OrdersData.objects.filter(delivery_date=delivery_date)
    if not deliveries.exists():
        raise ValueError("No delivery orders found for the specified date.")

    # Generate a cache key based on delivery_date, rider_names, and orders
    cache_key = _generate_cache_key(delivery_date, rider_names, deliveries)
    cache_entry = RoutePlanCache.objects.filter(delivery_date=delivery_date, rider_names_hash=cache_key).first()
    if cache_entry:
        logger.info("Using cached route plan.")
        return cache_entry.result_json

    # No cache found — continue with route planning
    unique_riders = list(set(rider_names))
    rider_histories = RiderHistoryData.objects.filter(rider_name__in=unique_riders)
    if rider_histories.count() != len(unique_riders):
        raise ValueError("Some rider histories were not found for the specified riders.")

    # Map rider names to their historical total distance
    rider_data = {r.rider_name: r.total_distance for r in rider_histories}

    # Get the origin coordinates
    origin = OriginData.objects.first()
    if not origin or not origin.latlng:
        raise ValueError("Origin data not found or is missing valid coordinates.")
    try:
        latlng_parts = origin.latlng.split(",")
        origin_latlng = [float(latlng_parts[0].strip()), float(latlng_parts[1].strip())]
    except Exception as e:
        logger.error("Error parsing origin coordinates: %s", e)
        raise ValueError("Invalid origin coordinates.")

    # Build delivery details and customer coordinate list
    delivery_data = []
    latlng_data = []
    for delivery in deliveries:
        customer_name = delivery.customer_name
        try:
            customer = CustomersData.objects.get(name=customer_name)
            lat, lng = map(float, customer.coordinate.split(","))
            delivery_data.append({
                "customer_name": customer.name,
                "latlng": customer.coordinate,
                "product": delivery.product,
                "address": delivery.address,
                "delivery_date": delivery.delivery_date.isoformat() if hasattr(delivery.delivery_date, "isoformat") else delivery.delivery_date,
                "origin": origin.name,
            })
            latlng_data.append((lat, lng))
        except CustomersData.DoesNotExist:
            delivery_data.append({
                "customer_name": customer_name,
                "latlng": None,
                "address": delivery.address,
                "product": delivery.product,
                "delivery_date": delivery.delivery_date.isoformat() if hasattr(delivery.delivery_date, "isoformat") else delivery.delivery_date,
                "origin": origin.name,
                "error": f"Customer data not found for {customer_name}"
            })

    # Perform clustering based on the number of riders
    if num_riders != 1:
        clustered = clustering.cluster(latlng_data, origin_latlng, num_riders)
    else:
        # If only one rider, create a full circular route (origin → deliveries → origin)
        origin_coords = [origin_latlng[0], origin_latlng[1]]
        customer_coords = [[float(lat), float(lng)] for lat, lng in latlng_data]
        clustered = [[origin_coords] + customer_coords + [origin_coords]]

    # Solve the TSP for each cluster
    routes = []
    for cluster_route in clustered:
        tsp_result = traveling_salesman_problem.process_tsp(origin_latlng, cluster_route)
        routes.append(tsp_result)  # tsp_result: (optimized_route, total_distance)

    # Sort routes by distance descending (longest first)
    routes.sort(key=lambda x: x[1], reverse=True)

    # Sort riders by historical distance ascending (least used first)
    sorted_riders = sorted(rider_data.items(), key=lambda x: x[1])
    assigned_routes = []
    rider_queue = list(sorted_riders)

    # Assign each route to a rider in a round-robin fashion
    for i, route in enumerate(routes):
        rider_name, _ = rider_queue[i % len(rider_queue)]
        assigned_routes.append({
            "rider_name": rider_name,
            "route": route[0],
            "distance": route[1]
        })

    # Final result
    result = {
        "deliveries": delivery_data,
        "latlng": [list(coord) for coord in latlng_data],
        "clusters": [[list(coord) for coord in cluster] for cluster in clustered],
        "routes": assigned_routes
    }

    # Convert delivery_date to a date object
    delivery_date_obj = datetime.strptime(delivery_date, "%Y-%m-%d").date()

    # Save the result to the cache
    RoutePlanCache.objects.create(
        delivery_date=delivery_date_obj,
        rider_names_hash=cache_key,
        result_json=json.loads(json.dumps(result, default=str))  
    )

    return result
