def dp(distance_matrix):
    n = len(distance_matrix)
    if n == 0:
        raise ValueError("Distance matrix must contain at least one city.")
    
    # dp_table[mask][i] represents the minimum cost to reach city i with the visited set of cities 'mask'
    dp_table = [[float('inf')] * n for _ in range(1 << n)]
    dp_table[1][0] = 0  # Starting from the origin (city 0)
    
    # Predecessor table for path reconstruction
    predecessor = [[-1] * n for _ in range(1 << n)]
    
    # Iterate over every subset of cities represented by bitmask
    for mask in range(1 << n):
        for u in range(n):
            if mask & (1 << u):  # City u is in the current subset 'mask'
                for v in range(n):
                    if not (mask & (1 << v)):  # City v is not visited in 'mask'
                        new_mask = mask | (1 << v)
                        new_cost = dp_table[mask][u] + distance_matrix[u][v]
                        if new_cost < dp_table[new_mask][v]:
                            dp_table[new_mask][v] = new_cost
                            predecessor[new_mask][v] = u

    final_mask = (1 << n) - 1  # All cities visited
    min_cost = float('inf')
    last_city = -1

    # Find the optimal cost to return to the origin (city 0)
    for u in range(1, n):
        total_cost = dp_table[final_mask][u] + distance_matrix[u][0]
        if total_cost < min_cost:
            min_cost = total_cost
            last_city = u

    # Reconstruct the optimal route sequence using the predecessor table
    sequence = []
    mask = final_mask
    while last_city != -1:
        sequence.append(last_city)
        next_city = predecessor[mask][last_city]
        mask ^= (1 << last_city)  # Remove last_city from the mask
        last_city = next_city

    sequence.reverse()  # Reverse to obtain the route from origin to destination
    
    return min_cost, sequence
