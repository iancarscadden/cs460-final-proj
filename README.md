# The Torchbearer

**Student Name:** Ian Carscadden
**Student ID:** 827329757
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

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

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source                                                                                                                            |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| S                | We start the route here, so we want the cheapest cost from S to every relic to decide which one to go at first.                               |
| Each relic       | After we visit a relic we want the cheapest cost from it to the remaining relics or the xit so every relic also have ot be a dijkstra source. |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property                    | Your answer                                                                                    |
| --------------------------- | ---------------------------------------------------------------------------------------------- |
| Data structure name         | nested dictionary                                                                              |
| What the keys represent     | outer key is source, inner is destination                                                      |
| What the values represent   | the cheapest fuel cost from source to destination                                              |
| Lookup time complexity      | O(1)                                                                                           |
| Why O(1) lookup is possible | python dicts are hash tables, so dist_table[u][v] is two hash lookups and each is O(1) average |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** `k + 1`, one from the spawn and one from each of the k relics
- **Cost per run:** O(m log n) using binary heap
- **Total complexity:** `O((k + 1) * m log n)` simplified -> `O(k * m log n)`
- **Justification (one line):** we run dikstra once per source and there are `k + 1` sources so the total cost is the `per run cost * num of source`

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  - dist[v] is the actual shortest path cost from x to v and it wont change.
  - The algorithm has confirmed there is no cheaper way to get there

- **For nodes not yet finalized (not in S):**
  - dist[u] is the cheapest path to u we have found so far but only using finalized nodes as the steps in between.
  - It can still get smaller once more nodes get added to S.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  - Before the first interation S will be empty so the "for every v in S" part is true. dist[x] is 0 since the empty path from x to iteslf has cost 0, and every other dist is infinity which matches "no path exists using only S-internal vertices" since there are no internal vertices to use yet.

- **Maintenance : why finalizing the min-dist node is always correct:**
  - When we pop the min-dist node u from outside S, dist[u] really is its shortest path. Any shorter path would have to leave S at some node w with dist[w] less than or equal to dist[u], but since edge weights are nonnegative the rest of the path from w to u cant make the total smaller, so no shorter path can exist.

- **Termination : what the invariant guarantees when the algorithm ends:**
  - Once the heap is empty every reachable node has been finalized, so the dist values are the shortest path costs from x. anything unreachable stays at infinity.

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

- If the distance table has wrong values then the route planner is optimizing over fake costs, so the order it picks might be more expensive than another order in the real graph.

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _Your answer here._
- **Counter-example setup:** _Your answer here._
- **What greedy picks:** _Your answer here._
- **What optimal picks:** _Your answer here._
- **Why greedy loses:** _Your answer here._

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _Your answer here._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component                | Variable name in code | Data type | Description |
| ------------------------ | --------------------- | --------- | ----------- |
| Current location         |                       |           |             |
| Relics already collected |                       |           |             |
| Fuel cost so far         |                       |           |             |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property                                    | Your answer      |
| ------------------------------------------- | ---------------- |
| Data structure chosen                       |                  |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected        | Time complexity: |
| Operation: unmark a relic (backtrack)       | Time complexity: |
| Why this structure fits                     |                  |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
