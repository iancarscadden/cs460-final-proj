# Development Log – The Torchbearer

**Student Name:** Ian Carscadden
**Student ID:** 827329757

---

## Entry 1 – 5/10/26: Initial Plan

This seems like a TSP variant where we have a directed graph and we need to hit every relic in a order between S and T.
My plan is to precompute shortest paths with dijkstra from S and each relic, then perform a recursive serach over relic orderings.
I think the lower bound for pruning is going to be the hardest part for me bc it cant overshoot the real remaining cost but still
cut branches. For testing i plan to start by using the cases provided and possibly build a graph where nearest neghibor gives a wrong
answer to ensure the search is not greedy.

---

## Entry 2 – 5/11/26: find_optimal_route + base recursive search

Implemented the find_optimal_route and \_explore without the pruning. I used a set for the relics_remaining since we want O(1) check, add, remove during the backtracking. I was confused by why the function used both relics_remaning and relics_visited_order since one could be derived via the other but i see that they serve different purposes. relics_remaining is used for fast membership during recursion and relics_visited_order is for building the final answer.

---

## Entry 3 – 5/12/26: Pruning + lower bound

Lower bound for pruning is cost_so_far + (remaining + 1) \* cheapest_edge, where cheapest_edge is the smallest value in the dist_table other than the zeros on the diagonal. cheapest_edge get computed once in find_optimal_route before any recursion. In \_explore i put it in best[2]. Solve function is in as well and all of the tests pass.

---

## Entry 4 – 5/12/26: Post-Implementation Reflection

All of tests from run_tests pass. The part i would keep building on is the lower bound. (remaining + 1) \* cheapest_edge works but its pretty loose since cheapest_edge is almost never the actual edge cost we use, so a lot of branches get expanded on that prob dont need to. A better version would use the cheapest incoming edge per relic but its more work.

---

## Final Entry – 5/12/26: Time Estimate

| Part                           | Estimated Hours |
| ------------------------------ | --------------- |
| Part 1: Problem Analysis       | 1hr             |
| Part 2: Precomputation Design  | 1hr             |
| Part 3: Algorithm Correctness  | 1.5 hr          |
| Part 4: Search Design          | 1.1 hr          |
| Part 5: State and Search Space | 2 hr            |
| Part 6: Pruning                | 1.5hr           |
| Part 7: Implementation         | 1hr             |
| README and DEVLOG writing      | 1hr             |
| **Total**                      | 10.1hr          |
