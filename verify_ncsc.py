r"""
Script to verify whether a family of blocks is a non-complete set covering nc(s,t,d,r).

A family C = (S_1, ..., S_r) of subsets of U_s = {0,...,s-1} is an nc(s,t,d,r) if
  (1) every t-subset of U_s is contained in at least one member of C, and
  (2) no at most d members of C cover U_s.
As in Definition 1 of the paper, members may be repeated.

Input files hold a Python/JSON list of blocks, e.g. [[0, 1, 2], [1, 3, 4], ...].
Points are labelled from 0, whereas the paper labels them from 1.
The parameters are read from the file name s_t_d_r.txt.

Usage:
    python3 verify_ncsc.py FILE [FILE ...]
"""
import argparse, json, os, re, sys


def parse_name(path):
    m = re.fullmatch(r"(\d+)_(\d+)_(\d+)_(\d+)", os.path.splitext(os.path.basename(path))[0])
    return tuple(map(int, m.groups())) if m else (None,) * 4


def uncovered_t_subset(s, t, blocks):
    """Returns a t-subset contained in no block, or None if all are covered."""
    # inc[p]: bitmask over block indices of the blocks containing point p
    inc = [0] * s
    for i, B in enumerate(blocks):
        for p in B:
            inc[p] |= 1 << i

    def rec(start, chosen, cand):
        if len(chosen) == t:
            return None
        for p in range(start, s - (t - len(chosen)) + 1):
            c = cand & inc[p]
            if not c:
                # any completion of this prefix is uncovered
                return chosen + [p]
            res = rec(p + 1, chosen + [p], c)
            if res:
                return res
        return None

    res = rec(0, [], (1 << len(blocks)) - 1)
    # pad to a full t-subset
    if res and len(res) < t:
        res += [q for q in range(s) if q not in res][: t - len(res)]
    return sorted(res) if res else None


def covering_d_tuple(s, d, blocks):
    """Returns the indices of at most d blocks whose union is U_s, or None."""
    full = (1 << s) - 1
    masks = [sum(1 << p for p in B) for B in blocks]
    by_point = [[i for i, M in enumerate(masks) if M >> p & 1] for p in range(s)]

    def rec(union, chosen):
        if union == full:
            return chosen
        if len(chosen) == d:
            return None
        # the lowest uncovered point must lie in one of the remaining chosen blocks
        p = (~union & full & -(~union & full)).bit_length() - 1
        for i in by_point[p]:
            res = rec(union | masks[i], chosen + [i])
            if res:
                return res
        return None

    return rec(0, [])


def verify(blocks, s, t, d, r=None):
    """Returns a list of (passed, message) pairs, one per checked condition."""
    errors = []
    sets = [frozenset(B) for B in blocks]
    if r is not None and len(blocks) != r:
        errors.append(f"expected r={r} blocks, found {len(blocks)}")
    for i, B in enumerate(blocks):
        if len(set(B)) != len(B):
            errors.append(f"block {i} has repeated points: {B}")
        bad = [p for p in B if not (isinstance(p, int) and 0 <= p < s)]
        if bad:
            errors.append(f"block {i} has points outside U_{s}: {bad}")
    if errors:
        return [(False, e) for e in errors]

    T = uncovered_t_subset(s, t, sets)
    D = covering_d_tuple(s, d, sets)
    return [
        (False, f"(1) {t}-subset {T} lies in no block") if T else
        (True, f"(1) every {t}-subset of U_{s} lies in some block"),
        (False, f"(2) the {len(D)} blocks {D} cover U_{s}") if D else
        (True, f"(2) no {d} blocks cover U_{s}"),
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()

    ok = True
    for path in args.files:
        s, t, d, r = parse_name(path)
        if s is None:
            print(f"SKIP  {path}: file name is not of the form s_t_d_r.txt")
            ok = False
            continue
        with open(path) as fh:
            blocks = json.load(fh)
        results = verify(blocks, s, t, d, r)
        label = f"nc({s},{t},{d},{len(blocks)})"
        if all(passed for passed, _ in results):
            print(f"OK    {path}: valid {label}")
        else:
            ok = False
            print(f"FAIL  {path}: not an {label}")
        for passed, msg in results:
            print(f"        [{'ok' if passed else 'FAIL'}] {msg}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
