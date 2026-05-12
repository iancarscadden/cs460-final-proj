# Development Log – The Torchbearer

**Student Name:** Ian Carscadden
**Student ID:** 827329757

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – [5/10/26]: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

This seems like a TSP variant where we have a directed graph and we need to hit every relic in a order between S and T.
My plan is to precompute shortest paths with dijkstra from S and each relic, then perform a recursive serach over relic orderings.
I think the lower bound for pruning is going to be the hardest part for me bc it cant overshoot the real remaining cost but still
cut branches. For testing i plan to start by using the cases provided and possibly build a graph where nearest neghibor gives a wrong
answer to ensure the search is not greedy.

---

## Entry 2 – [5/11/26]: [Short description]

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

Implemented the find_optimal_route and \_explore without the pruning. I used a set for the relics_remaining since we want O(1) check, add, remove during the backtracking. I was confused by why the function used both relics_remaning and relics_visited_order since one could be derived via the other but i see that they serve different purposes. relics_remaining is used for fast membership during recursion and relics_visited_order is for building the final answer. Also ran tests to verify passing then reverted solve() back to pass.

---

## Entry 3 – [Date]: [Short description]

_Your entry here._

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part                           | Estimated Hours |
| ------------------------------ | --------------- |
| Part 1: Problem Analysis       | 1hr             |
| Part 2: Precomputation Design  | 1hr             |
| Part 3: Algorithm Correctness  | 1.5 hr          |
| Part 4: Search Design          | 1.1 hr          |
| Part 5: State and Search Space | 2 hr            |
| Part 6: Pruning                |                 |
| Part 7: Implementation         |                 |
| README and DEVLOG writing      |                 |
| **Total**                      |                 |
