# The Torchbearer

**Student Name:** Ian Carscadden
**Student ID:** 827329757
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  Dijkstra from S can give us the cheapest cost to get to every node from S, but it cant decide whic relic to visit first.
  Once you pick the first relic, every cost after that starts from the relic, not S, so a single run from S will miss every cost
  past the first hop.

- **What decision remains after all inter-location costs are known:**
  The decision that remains is the order to visit the certain relics in. The cost table is just for lookup at this point, so the
  actual optimization is picking the permutation of relics between S and T so we minimize the sum of the looksups.

- **Why this requires a search over orders (one sentence):**
  Different visit orders give different totals and the costs alone can't tell us which permutation wins, so will have to serach
  over relic orderings instead of computer answer directly.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source                                                                                                                             |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| S                | We start the route here, so we want the cheapest cost from S to every relic to decide which one to go at first.                                |
| Each relic       | After we visit a relic we want the cheapest cost from it to the remaining relics or the exit so every relic also have to be a dijkstra source. |

### Part 2b: Distance Storage

| Property                    | Your answer                                                                                    |
| --------------------------- | ---------------------------------------------------------------------------------------------- |
| Data structure name         | nested dictionary                                                                              |
| What the keys represent     | outer key is source, inner is destination                                                      |
| What the values represent   | the cheapest fuel cost from source to destination                                              |
| Lookup time complexity      | O(1)                                                                                           |
| Why O(1) lookup is possible | python dicts are hash tables, so dist_table[u][v] is two hash lookups and each is O(1) average |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** `k + 1`, one from the spawn and one from each of the k relics
- **Cost per run:** O(m log n) using binary heap
- **Total complexity:** `O((k + 1) * m log n)` simplified -> `O(k * m log n)`
- **Justification (one line):** we run dikstra once per source and there are `k + 1` sources so the total cost is the `per run cost * num of source`

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  - dist[v] is the actual shortest path cost from x to v and it wont change.
  - The algorithm has confirmed there is no cheaper way to get there

- **For nodes not yet finalized (not in S):**
  - dist[u] is the cheapest path to u we have found so far but only using finalized nodes as the steps in between.
  - It can still get smaller once more nodes get added to S.

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
  - Before the first interation S will be empty so the "for every v in S" part is true. dist[x] is 0 since the empty path from x to iteslf has cost 0 and every other dist is infinity which matches "no path exists using only S-internal vertices" since there are no internal vertices to use yet.

- **Maintenance : why finalizing the min-dist node is always correct:**
  - When we pop the min-dist node u from outside S, dist[u] really is its shortest path. Any shorter path would have to leave S at some node w with dist[w] less than or equal to dist[u], but since edge weights are nonnegative the rest of the path from w to u cant make the total smaller, so no shorter path can exist.

- **Termination : what the invariant guarantees when the algorithm ends:**
  - Once the heap is empty every reachable node has been finalized, so the dist values are the shortest path costs from x. anything unreachable stays at infinity.

### Part 3c: Why This Matters for the Route Planner

- If the distance table has wrong values then the route planner is optimizing over fake costs, so the order it picks might be more expensive than another order in the real graph.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** Nearest neighbor greedy will pick the cheapest next relic from wherever we currently are. This will break when the cheapest first hop puts us in a spot where everything after is a lot for expensive.
- **Counter-example setup:** Say we have two relics, A and B, with parwise costs S -> A = 4, S -> B = 6, A -> B = 67, A -> T = 4, B -> A = 4, B -> T = 56. Each relic has one cheap outgoing edge but they go to different places. A's cheap edge goes to T and B's cheap edge goes to A.
- **What greedy picks:** Greedy goes S -> A first since A is the cheapest from S. Then from A it has to take A -> B to grab B, then B -> T to get another 56, for total 4 + 67 + 56 = 127.
- **What optimal picks:** Optimal is S -> B -> A -> T = 6 + 4 + 4 = 14. the order [B, A] lets you use each relics cheap outgoing edge.
- **Why greedy loses:** Greedy saves 2 unit by picking A over B at the start, but it lost 115 next because going to A first forced the expensive A -> B and B -> T edges.

### What the Algorithm Must Explore

- The algo has to try different orders of the relics between S and T since the cheapest total cost isnt determined by any single local choice its the sum across the whole sequence.

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component                | Variable name in code | Data type     | Description                                                   |
| ------------------------ | --------------------- | ------------- | ------------------------------------------------------------- |
| Current location         | current_loc           | node          | the relic or spawn the torchbearer is currently positioned at |
| Relics already collected | relics_visited_order  | list of nodes | ordered list of relics visited so far in the recursion flow   |
| Fuel cost so far         | cost_so_far           | int/float     | total fuel burned to reach current_loc                        |

### Part 5b: Data Structure for Visited Relics

| Property                                    | Your answer                                                                                                                       |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Data structure chosen                       | set                                                                                                                               |
| Operation: check if relic already collected | Time complexity: O(1) average                                                                                                     |
| Operation: mark a relic as collected        | Time complexity: O(1) average                                                                                                     |
| Operation: unmark a relic (backtrack)       | Time complexity: O(1) average                                                                                                     |
| Why this structure fits                     | hash set gives O(1) average for membership check, add, and remove, and all three happen constantly during the backtracking search |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k!
- **Why:** at the top of the serach we pick any of the k relics to visit first then any of the remaining k-1, then k-2, etc the way down, which gives `k * (k-1) * ... * 1 = k!` orderings

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** The lowest total fuel cost of any complete route from S through all relics to T we have found so far plus the orderings of the relics that produced it. Stored in best[0] and best[1]
- **When it is used:** At the top of every recursive call we compare a lower bound on the current branch against best[0], and we also compare against best when a newly completed route is found to see if its an improvement
- **What it allows the algorithm to skip:** Any partial route whose lowest possible completion cant beat best gets cut off without expanding deeper.

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** cost_so_far, current_loc, the set of remaining relics, the dist_table, and the precomputed cheapest_edge stashed in best[2]
- **What the lower bound accounts for:** We still need remaining + 1 more hops to finish, one per remaining relics plus one to the exit, and each hop costs at least cheapest_edge. so cost_so_far + (remaining + 1) \* cheapest_edge is the lowest the total could come out to.
- **Why it never overestimates:** Every valid continuation has to use at least that many hops and every hop is at least cheapest_edge, so the real final cost can never come in below the bound.

### Part 6c: Pruning Correctness

- if the lower bound on completing this branch is already >= best then every possible completion would also be >= best.
- Skipping this branch cant cause us to lose the optimal since the optimal would have to come in stictly below best to win and we just proved nothing in this branch can.

---

## References

- Lecture notes
