# New non-complete set coverings

This repository contains the explicit coverings behind the upper bounds of

> E. Piccione and J. Vorloeper, *Applying Combinatorial Techniques To Find Minimal Non-Complete Set Coverings*.

Every upper bound on $\rho_{t,d}(s)$ marked by a cross in Figure 1 of the paper is attained by one of the files below, and every file is such a cross.
The repository also contains a script that checks the files against the definition.

## Definition

A family $\mathcal C = (S_1, \dots, S_r)$ of subsets of $U_s$ is an $\mathrm{nc}(s,t,d,r)$ if

1. every $t$-subset of $U_s$ is contained in at least one member of $\mathcal C$, and
2. no $d$ or fewer members of $\mathcal C$ have union $U_s$.

Members may repeat and may have fewer than $t$ elements, but none of the files below contain repeated members or members with fewer than $t$ elements.

## File format

Each file `s_t_d_r.txt` holds one $\mathrm{nc}(s,t,d,r)$ as a JSON list of $r$ members, for example

```
[[0, 1, 2, 6, 8], [0, 1, 3, 4, 5], ...]
```

**Note:** Points are labelled $0, \dots, s-1$, whereas the paper uses $U_s = \{1, \dots, s\}$; add $1$ to every point to obtain the paper's labelling.
The files are sorted into folders `t_d/` by degree $t$ and order $d$.

## Verifying the coverings

`verify_ncsc.py` reads $s, t, d, r$ from the file name and checks

- that the file contains exactly $r$ members, each a set of points in $\{0, \dots, s-1\}$,
- condition 1, by searching for a $t$-set that lies in no member, and
- condition 2, by searching for at most $d$ members covering all points.

Both searches are exhaustive.
If a condition fails, the script prints a counterexample.
Its only dependency is Python 3.8+.

To check a single file or all of them:

```bash
python3 verify_ncsc.py 3_3/18_3_3_18.txt
python3 verify_ncsc.py */*.txt
```

Example output:

```
OK    3_3/18_3_3_18.txt: valid nc(18,3,3,18)
        [ok] (1) every 3-subset of U_18 lies in some block
        [ok] (2) no 3 blocks cover U_18
```

The script exits with status 0 if every file passes and 1 otherwise.
Checking all files takes a few seconds.

