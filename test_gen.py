# from sympy import primerange

# def nth_prime(n):
#     """Return the nth prime (1-based)."""
#     primes = list(primerange(1, 1000))
#     return primes[n - 1]

# def generate_arrays(N):
#     target_sum = 2 * N - 2
#     max_arrays = nth_prime(N - 2)

#     results = []

#     def backtrack(remaining, length, max_val, current):
#         # If array complete
#         if length == 0:
#             if remaining == 0:
#                 results.append(current[:])
#             return

#         # Try values in descending order
#         for v in range(min(max_val, remaining), 0, -1):
#             if v >= N:
#                 continue

#             # Ensure enough remaining for future 1's
#             if remaining - v < length - 1:
#                 continue

#             current.append(v)
#             backtrack(
#                 remaining - v,
#                 length - 1,
#                 v,  # enforce non-increasing order (uniqueness)
#                 current
#             )
#             current.pop()

#             if len(results) >= max_arrays:
#                 return

#     backtrack(target_sum, N, N - 1, [])

#     return results


# # Example
# N = 5
# arrays = generate_arrays(N)

# print(f"Generated {len(arrays)} arrays for N={N}:")
# for arr in arrays:
#     print(arr)


# best so far

# def generate_hand_pruned(N):
#     target_sum = 2 * N - 2
#     start_array = [target_sum - (N - 1)] + [1] * (N - 1)

#     seen = set()
#     results = []

#     stats = {
#         "arrays_explored": 0,
#         "redistributions_attempted": 0,
#         "unique_arrays_found": 0
#     }

#     def recurse(arr):
#         t = tuple(arr)
#         if t in seen:
#             return
#         seen.add(t)
#         results.append(arr[:])
#         stats["arrays_explored"] += 1
#         stats["unique_arrays_found"] += 1

#         # Iterate over array to find "useful" numbers
#         for i in range(len(arr)):
#             if arr[i] <= 1:
#                 continue  # cannot redistribute from 1
#             if i > 0 and arr[i] <= arr[i-1]:
#                 continue  # number is blocked by a larger/equal number before it

#             # Find first smaller number ahead to redistribute
#             for j in range(i + 1, len(arr)):
#                 if arr[j] >= arr[i]:
#                     continue  # cannot add to a number bigger or equal
#                 if arr[j] >= N - 1:
#                     continue  # cannot exceed N-1
#                 stats["redistributions_attempted"] += 1
#                 new_arr = arr[:]
#                 new_arr[i] -= 1
#                 new_arr[j] += 1
#                 new_arr.sort(reverse=True)
#                 recurse(new_arr)  # recursive call

#     recurse(start_array)
#     return results, stats


# # Example usage
# N = 8
# arrays, stats = generate_hand_pruned(N)

# arrays_sorted = sorted(arrays, key=lambda x: x[0], reverse=True)

# print(f"Generated {len(arrays_sorted)} arrays for N={N} (pruned hand-like recursive):")
# for arr in arrays_sorted:
#     print(arr)

# print("\nStats:")
# for k, v in stats.items():
#     print(f"{k}: {v}")




def redistribution_based(N):
    target_sum = 2 * N - 2
    start_array = [target_sum - (N - 1)] + [1] * (N - 1)
    seen = set()
    results = []
    stats = {"nodes_generated": 0, "nodes_expanded": 0, "nodes_pruned_duplicate": 0}

    def recurse(arr):
        stats["nodes_generated"] += 1
        t = tuple(arr)
        if t in seen:
            stats["nodes_pruned_duplicate"] += 1
            return
        seen.add(t)
        results.append(arr[:])
        stats["nodes_expanded"] += 1

        for i in range(len(arr)):
            if arr[i] <= 1:
                continue
            if i > 0 and arr[i] <= arr[i - 1]:
                continue
            for j in range(i + 1, len(arr)):
                if arr[j] >= arr[i]:
                    continue
                if arr[j] >= N - 1:
                    continue
                new_arr = arr[:]
                new_arr[i] -= 1
                new_arr[j] += 1
                new_arr.sort(reverse=True)
                recurse(new_arr)

    recurse(start_array)
    return results, stats


# def tree_degree_sequences_optimal(n):
#     target = 2 * (n - 1)
#     results = []
#     stats = {"nodes_generated": 0, "nodes_expanded": 0, "dead_ends": 0}

#     def build(rem_sum, rem_slots, max_val, current):
#         stats["nodes_generated"] += 1

#         if rem_slots == 0:
#             stats["nodes_expanded"] += 1
#             results.append(current[:])
#             return

#         # Tight bounds — mathematically guaranteed no dead ends within these
#         lo = max(1, -((-rem_sum) // rem_slots))  # ceil(rem_sum / rem_slots)
#         hi = min(max_val, rem_sum - rem_slots + 1)  # leave at least 1 for each remaining slot

#         if lo > hi:           # only triggers if max_val is too small (shouldn't happen
#             stats["dead_ends"] += 1   # with correct initial call, kept for safety)
#             return

#         stats["nodes_expanded"] += 1
#         for val in range(hi, lo - 1, -1):
#             current.append(val)
#             build(rem_sum - val, rem_slots - 1, val, current)
#             current.pop()

#     build(target, n, target, [])
#     return results, stats

def _make_initial(target_sum, N, deg_cap):
    # dont let any of the elements of the array bigger than deg_cap, but the sum must still reach target_sum
    arr = [1] * N
    arr[0] = target_sum - (N - 1)
    for i in range(N):
        if arr[i] > deg_cap:
            excess = arr[i] - deg_cap
            arr[i] = deg_cap
            if i + 1 < N:
                arr[i + 1] += excess
    return arr


def redistribution_based(N, n_ary=None, m_ary=None):
    if n_ary is None:
        n_ary = N - 1
    deg_cap = n_ary
    target_sum = 2 * N - 2

    start_array = _make_initial(target_sum, N, deg_cap + 1)
    seen = set()
    results = []
    stats = {"generated": 0, "pruned_dup": 0, "pruned_depth": 0}

    def recurse(arr):
        stats["generated"] += 1
        t = tuple(arr)
        if t in seen:
            stats["pruned_dup"] += 1
            return
        seen.add(t)

        # Depth feasibility check
        if m_ary is not None and min_possible_depth(arr, n_ary) > m_ary:
            stats["pruned_depth"] += 1
            return  # ← prunes this node AND all descendants

        results.append(arr[:])

        for i in range(len(arr)):
            if arr[i] <= 1:
                continue
            if i > 0 and arr[i] <= arr[i - 1]:
                continue
            for j in range(i + 1, len(arr)):
                if arr[j] >= arr[i]:
                    continue
                if arr[j] >= deg_cap:
                    continue
                new_arr = arr[:]
                new_arr[i] -= 1
                new_arr[j] += 1
                new_arr.sort(reverse=True)
                recurse(new_arr)

    recurse(start_array)
    return results, stats


def min_possible_depth(degree_seq, n_ary):
    """Lower bound on min rooted depth across all trees realizing this degree sequence."""
    degs = sorted(degree_seq, reverse=True)
    N = len(degs)
    if N <= 1:
        return 0
    
    best = float('inf')
    seen_root_degs = set()

    # Try each distinct degree value as root candidate
    for root_idx in range(N):
        root_deg = degs[root_idx]
        if root_deg > n_ary:
            continue  # root can't have more than n_ary children
        seen_root_degs.add(root_deg)
        if root_deg > n_ary:
            continue
        others = degs[:root_idx] + degs[root_idx+1:]
        # Each non-root contributes (deg - 1) children slots
        child_capacity = sorted([d - 1 for d in others], reverse=True)
        
        depth = 0
        slots = root_deg
        idx = 0
        remaining = len(others)
        
        while remaining > 0:
            depth += 1
            if slots == 0:
                depth = float('inf')
                break
            placed = min(slots, remaining)
            slots = sum(child_capacity[idx:idx+placed])
            idx += placed
            remaining -= placed
        
        best = min(best, depth)
    return best

if __name__ == "__main__":
    N = 6
    n_ary = 5
    m_ary = 3
    arrays, stats = redistribution_based(N, n_ary, m_ary)
    for a in arrays:
        print(a)
        
    # print(_make_initial(20, 7, 3))
    # # --- three-way comparison ---
    # print(f"{'N':>4} | {'res':>5} || "
    #     f"{'opt gen':>9} {'opt exp':>9} {'opt dead':>9} || "
    #     f"{'red gen':>9} {'red exp':>9} {'red dup':>9}")
    # print("-" * 95)

    # for N in [4, 6, 8, 10, 12, 14, 16, 20, 25, 30, 40, 50]:
    #     # r1, s1 = tree_degree_sequences_optimal(N)
    #     r2, s2 = redistribution_based(N)          # your algorithm
    #     # r3, s3 = generate_hand_pruned(N)
    #     print(f"{N:>4} | {len(r1):>5} || "
    #         # f"{s1['nodes_generated']:>9} {s1['nodes_expanded']:>9} {s1['dead_ends']:>9} || "
    #         f"{s2['nodes_generated']:>9} {s2['nodes_expanded']:>9} {s2['nodes_pruned_duplicate']:>9}")
    #         #   f"{s3['nodes_generated']:>9} {s3['arrays_explored']:>9} {s3['unique_arrays_found']:>9}")