"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Ian Carscadden
Student ID:   827329757

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    """
    Q1 = "Dijkstra from S can give us the cheapest cost to get to every node from S, but it cant decide whic relic to visit first. Once you pick the first relic, every cost after that starts from the relic, not S, so a single run from S will miss every cost past the first hop."
    Q2 = " The decision that remains is the order to visit the certain relics in. The cost table is just for lookup at this point, so the actual optimization is picking the permutation of relics between S and T so we minimize the sum of the looksups."
    Q3 = " Different visit orders give different totals and the costs alone can't tell us which permutation wins, so will have to serach over relic orderings instead of computer answer directly."
    return Q1 + Q2 + Q3


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    """
    # the exit is never a source since we dont travel out of it
    # so we need to run dijkstra from the spawn and each relic
    sources = [spawn]
    for r in relics:
        if r not in sources:
            sources.append(r)
    return sources


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    """
    # dijkstra with min-heap, we have non-neg edge costs
    # this should give us shortest path from source to every reachable node

    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    heap = [(0, source)]

    while heap:
        cost, u = heapq.heappop(heap)
        if cost > dist[u]:
            continue
        for v, w in graph[u]:
            new_cost = cost + w
            if new_cost < dist[v]:
                dist[v] = new_cost
                heapq.heappush(heap, (new_cost, v))
    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    """
    # run dijkstra from every source in select_sources
    # store the results in nested dict for dist_table[u][v] later
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    for s in sources:
        dist_table[s] = run_dijkstra(graph, s)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """
    Q1 = "dist[v] is the actual shortest path cost from x to v and it wont change."
    Q2 = " The algorithm has confirmed there is no cheaper way to get there"
    Q3 = " dist[u] is the cheapest path to u we have found so far but only using finalized nodes as the steps in between."
    Q4 = " It can still get smaller once more nodes get added to S."
    Q5 = " Before the first interation S will be empty so the \"for every v in S\" part is true. dist[x] is 0 since the empty path from x to iteslf has cost 0 and every other dist is infinity which matches \"no path exists using only S-internal vertices\" since there are no internal vertices to use yet."
    Q6 = " When we pop the min-dist node u from outside S, dist[u] really is its shortest path. Any shorter path would have to leave S at some node w with dist[w] less than or equal to dist[u], but since edge weights are nonnegative the rest of the path from w to u cant make the total smaller, so no shorter path can exist."
    Q7 = " Once the heap is empty every reachable node has been finalized, so the dist values are the shortest path costs from x. anything unreachable stays at infinity."
    Q8 = " If the distance table has wrong values then the route planner is optimizing over fake costs, so the order it picks might be more expensive than another order in the real graph."
    
    return Q1 + Q2 + Q3 + Q4 + Q5 + Q6 + Q7 + Q8


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """

    Q1 = "Nearest neighbor greedy will pick the cheapest next relic from wherever we currently are. This will break when the cheapest first hop puts us in a spot where everything after is a lot for expensive."
    Q2 = " Say we have two relics, A and B, with parwise costs S -> A = 4, S -> B = 6, A -> B = 67, A -> T = 4, B -> A = 4, B -> T = 56. Each relic has one cheap outgoing edge but they go to different places. A's cheap edge goes to T and B's cheap edge goes to A."
    Q3 = " Greedy goes S -> A first since A is the cheapest from S. Then from A it has to take A -> B to grab B, then B -> T to get another 56, for total 4 + 67 + 56 = 127."
    Q4 = " Optimal is S -> B -> A -> T = 6 + 4 + 4 = 14. the order [B, A] lets you use each relics cheap outgoing edge."
    Q5 = " Greedy saves 2 unit by picking A over B at the start, but it lost 115 next because going to A first forced the expensive A -> B and B -> T edges."
    Q6 = " The algo has to try different orders of the relics between S and T since the cheapest total cost isnt determined by any single local choice its the sum across the whole sequence."

    return Q1 + Q2 + Q3 + Q4 + Q5 + Q6


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    # handle edge case of no relics go straight from spawn to exit
    if not relics:
        if exit_node in dist_table.get(spawn, {}):
            return (dist_table[spawn][exit_node], [])
        return (float('inf'), [])

    # find the cheapest pairwise cost in the table to use as a floor
    # in pruning lower bound
    cheapest_edge = float('inf')
    for src in dist_table.values():
        for d in src.values():
            if 0 < d < cheapest_edge:
                cheapest_edge = d

    best = [float('inf'), [], cheapest_edge]
    relics_remaining = set(relics)

    _explore(dist_table, spawn, relics_remaining, [], 0, exit_node, best)
    return (best[0], best[1])



def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.
    """
    # base case every relic collected take the final hop to exit
    if not relics_remaining:
        if exit_node not in dist_table[current_loc]:
            return
        total  = cost_so_far + dist_table[current_loc][exit_node]
        if total < best[0]:
            best[0] = total
            best[1] = list(relics_visited_order)
        return

    # pruning
    # we still need remaining + 1 more hops to finish and each hop costs at least
    # cheapest_edge, so cost_so_far + (remaining + 1) * cheapest_edge is the lowest
    # the total could come out to. if that lower bound is already >= best then
    # nothing in this branch can beat best so we can return early 
    cheapest_edge = best[2]
    hops_needed = len(relics_remaining) + 1
    lower_bound = cost_so_far + hops_needed * cheapest_edge
    if lower_bound >= best[0]:
        return        

    # recursive case try each remanining relic as the next stop
    for r in list(relics_remaining):
        if r not in dist_table[current_loc]:
            continue
        step_cost = dist_table[current_loc][r]
        relics_remaining.remove(r)
        relics_visited_order.append(r)
        _explore(dist_table, r, relics_remaining, relics_visited_order, cost_so_far + step_cost, exit_node, best)
        relics_visited_order.pop()
        relics_remaining.add(r)



# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)
   


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
    
    