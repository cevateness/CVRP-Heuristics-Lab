import numpy as np 


### 2-Opt Local Search Function
def apply_2opt(edge_weight, route,max_no_improvement=1500):
    """
    Apply the 2-opt algorithm to improve a given route by reversing segments of the route.
    
    Parameters:
    - edge_weight: A matrix representing the distances between nodes.
    - route: A list representing the sequence of nodes in the route.
    - max_no_improvement: The number of iterations with no improvement before stopping.
    
    Returns:
    - best_route: The improved route after applying 2-opt.
    """
    best_route = route
    best_cost = calculate_route_cost(edge_weight, best_route)
    no_improvement_counter = 0
    
    while no_improvement_counter < max_no_improvement:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                if j - i == 1:  # Skip consecutive nodes as it would result in no change
                    continue
                
                # Create a new route by reversing the segment between i and j
                new_route = best_route[:i] + best_route[i:j][::-1] + best_route[j:]

                new_cost = calculate_route_cost(edge_weight, new_route)
                
                if new_cost < best_cost:
                    best_route = new_route
                    best_cost = new_cost
                    improved = True
        
        if improved:
            no_improvement_counter = 0  # Reset counter if there was an improvement
        else:
            no_improvement_counter += 1  # Increment counter if no improvement was found
    
    return best_route

def calculate_route_cost(edge_weight, route, include_depot=True):
    cost = 0
    # Include the cost from the depot to the first node if specified
    if include_depot and len(route) > 0:
        cost += edge_weight[0, route[0]]

    # Sum the cost of the route between consecutive nodes
    for i in range(len(route) - 1):
        cost += edge_weight[route[i], route[i + 1]]
    
    # Include the cost of returning to the depot from the last node if specified
    if include_depot and len(route) > 0:
        cost += edge_weight[route[-1], 0]
    
    return cost

def nearest_neighbor_with_2opt(instance):
    n = len(instance["demand"])
    visited = np.zeros(n, dtype=bool)  # Track visited nodes
    routes = {}
    route_index = 0
    depot = 0  # Assuming the depot is at index 0
    
    while not all(visited[1:]):  # Continue until all customers are visited
        current_route = []
        current_load = 0
        current_node = depot
        
        while True:
            nearest_node = None
            nearest_distance = float('inf')
            
            # Find the nearest unvisited customer that can be added without exceeding capacity
            for i in range(1, n):
                if not visited[i] and instance["demand"][i] + current_load <= instance["capacity"]:
                    distance = instance["edge_weight"][current_node][i]
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest_node = i
            
            if nearest_node is None:  # No more customers can be added to this route
                break
            
            # Add the nearest customer to the route
            current_route.append(nearest_node)
            current_load += instance["demand"][nearest_node]
            visited[nearest_node] = True
            current_node = nearest_node
        

        # Apply 2-opt local search to improve the route
        optimized_route = apply_2opt(instance["edge_weight"], current_route)
        routes[route_index] = optimized_route
        route_index += 1
    
    return routes
