"""Reproduce default-stack limits in fresh direct/check_slides processes.

Successful observations must finish within --timeout seconds. Timeouts are
reported separately: they are never claimed to be recursion boundaries.
"""

import argparse
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_slides.py"
WINDOW = """def to_n(n):
    result = ZERO
    for _ in range(n):
        result = SUCC(result)
    return result
"""
PREFIX_WINDOW = """to_stop = StopIteration()
def to_tick(x):
    global to_depth
    import sys
    frame = sys._getframe()
    to_depth = 0
    while frame is not None:
        to_depth += 1
        frame = frame.f_back
    raise to_stop
def to_int(n):
    return n(to_tick)(0)
"""


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def observation(kind, n, divisor=None):
    value = f"to_n({n})"
    if kind == "FACT":
        return f"to_int(FACT({value}))", math.factorial(n)
    if kind == "SUM_TO_N":
        return f"to_int(SUM_TO_N({value}))", n * (n + 1) // 2
    if kind == "FIB":
        return f"to_int(FIB({value}))", fibonacci(n)
    if kind == "SUCC":
        return f"to_int({value})", n
    if kind == "RANGE":
        return f"to_list(RANGE(ONE)({value}), to_int)", list(range(1, n + 1))
    if kind == "SUM_RANGE":
        return f"to_int(SUM(RANGE(ONE)({value})))", n * (n + 1) // 2
    if kind == "FIZZBUZZ":
        expected = [("Fizz" if x % 3 == 0 else "")
                    + ("Buzz" if x % 5 == 0 else "") or str(x)
                    for x in range(1, n + 1)]
        return f"to_list(FIZZBUZZ({value}), to_str)", expected
    if kind in {"MOD", "DIV"}:
        ds = [divisor] if divisor is not None else range(1, 8)
        expressions = [f"to_int({kind}({value})(to_n({d})))" for d in ds]
        results = [n % d if kind == "MOD" else n // d for d in ds]
        return "[" + ", ".join(expressions) + "]", results
    if kind == "POW_TWO":
        return f"to_int(POW(TWO)({value}))", 2 ** n
    if kind == "POW_BASE":
        return f"to_int(POW({value})(FOUR))", n ** 4
    if kind == "TO_DIGITS":
        return f"to_str(TO_DIGITS({value}))", str(n)
    raise ValueError(kind)


def probe(kind, n, mode, timeout, divisor=None, prefix=False):
    expression, expected = observation(kind, n, divisor)
    if mode == "direct":
        source = ("import sys, time, json\n"
                  f"sys.path.insert(0, {str(ROOT / 'code')!r})\n"
                  "from lambda_core import *\n"
                  + WINDOW
                  + (PREFIX_WINDOW if prefix else "")
                  + "assert sys.getrecursionlimit() == 1000\n"
                  + "started = time.perf_counter()\ntry:\n"
                  + f"    result = {expression}\n"
                  + f"    assert result == {expected!r}\n"
                  + "    status = 'ok'\n"
                  + "except StopIteration:\n"
                  + "    status = 'ok'\n"
                  + "except RecursionError:\n"
                  + "    status = 'recursion'\n"
                  + "print(json.dumps({'status': status, "
                    "'seconds': time.perf_counter() - started}))\n")
        cmd = [sys.executable, "-c", source]
        temp = None
    else:
        observed = (f">>> {expression}\n"
                    "Traceback (most recent call last):\n  ...\n"
                    "StopIteration\n" if prefix and expected != 0 else
                    f">>> {expression} == {expected!r}\nTrue\n")
        markdown = ("```python\n" + WINDOW + "```\n"
                    + ("```python\n" + PREFIX_WINDOW + "```\n"
                       if prefix else "")
                    +
                    "```python\n"
                    "def to_clock():\n"
                    "    import time\n"
                    "    return time.perf_counter()\n"
                    "def to_report(elapsed):\n"
                    "    print('TIMING', elapsed)\n"
                    "```\n"
                    "```python\n"
                    ">>> to_started = to_clock()\n"
                    + observed +
                    ">>> to_elapsed = to_clock() - to_started\n"
                    "```\n"
                    "```python\nto_report(to_elapsed)\n```\n")
        temp = tempfile.NamedTemporaryFile(mode="w", suffix=".md",
                                           encoding="utf-8", delete=False)
        temp.write(markdown)
        temp.close()
        cmd = [sys.executable, str(CHECKER), temp.name, "--preload-core"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                timeout=timeout, cwd=ROOT)
        if mode == "direct":
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            return json.loads(result.stdout)
        timing = next((line.split()[1] for line in result.stdout.splitlines()
                       if line.startswith("TIMING ")), None)
        if result.returncode == 0:
            return {"status": "ok", "seconds": float(timing)}
        if "RecursionError" in result.stdout:
            return {"status": "recursion", "seconds": float(timing)}
        raise RuntimeError(result.stdout + result.stderr)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "seconds": timeout}
    finally:
        if temp is not None:
            Path(temp.name).unlink(missing_ok=True)


def boundary(kind, mode, timeout, divisor=None, prefix=False):
    cache = {}

    def at(n):
        if n not in cache:
            cache[n] = probe(kind, n, mode, timeout, divisor, prefix)
        return cache[n]["status"] == "ok"

    low, high = 0, 1
    assert at(0)
    while at(high):
        low, high = high, high * 2
    while high - low > 1:
        middle = (low + high) // 2
        if at(middle):
            low = middle
        else:
            high = middle
    # Repeat both sides in fresh processes and record the actual observations.
    success = probe(kind, low, mode, timeout, divisor, prefix)
    failure = probe(kind, high, mode, timeout, divisor, prefix)
    if failure["status"] == "ok":
        # Wall-clock time varies with machine load near the timeout.
        while failure["status"] == "ok":
            low, success = high, failure
            high += 1
            failure = probe(kind, high, mode, timeout, divisor, prefix)
            cache[high] = failure
    if success["status"] != "ok":
        if success["status"] != "timeout":
            raise RuntimeError(f"Unstable stack boundary: {kind} {mode}")
        success = cache[low]
    earlier_trials = {}
    for n, result in ((low, success), (high, failure)):
        if n in cache and cache[n]["status"] != result["status"]:
            earlier_trials[str(n)] = cache[n]
        cache[n] = result
    return {"largest_completed": low, "next_n": high,
            "next_status": failure["status"],
            "seconds_at_largest": success["seconds"],
            "earlier_trials": earlier_trials,
            "probes": {str(n): result for n, result in sorted(cache.items())}}


def verify_prefix_profile():
    """Compare the whole observation's peak with its first increment."""
    source = ("import json, sys\n"
              f"sys.path.insert(0, {str(ROOT / 'code')!r})\n"
              "from lambda_core import *\n"
              "to_core_int = to_int\n" + WINDOW + PREFIX_WINDOW + """
reports = []
for kind, ns in [('FACT', range(9)), ('POW_TWO', range(11)),
                 ('POW_BASE', range(1, 9))]:
    for n in ns:
        if kind == 'FACT':
            value = FACT(to_n(n))
        elif kind == 'POW_TWO':
            value = POW(TWO)(to_n(n))
        else:
            value = POW(to_n(n))(FOUR)
        to_max_depth = 0
        def to_profile(frame, event, arg):
            global to_max_depth
            if event == 'call':
                depth = 0
                while frame is not None:
                    depth += 1
                    frame = frame.f_back
                to_max_depth = max(to_max_depth, depth)
        sys.setprofile(to_profile)
        actual = to_core_int(value)
        sys.setprofile(None)
        try:
            to_int(value)
        except StopIteration:
            pass
        reports.append(dict(kind=kind, n=n, result=actual,
                            full_peak=to_max_depth,
                            first_tick_depth=to_depth))
        assert to_max_depth == to_depth, reports[-1]
print(json.dumps(reports))
""")
    result = subprocess.run([sys.executable, "-c", source],
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--stack-prefix", action="store_true",
                        help="FACT/POW: stop at the first integer tick")
    parser.add_argument("--verify-prefix-profile", action="store_true",
                        help="compare full/prefix stack profiles on small cases")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "plan" / "limits.json")
    parser.add_argument("--kinds", nargs="+", default=[
        "FACT", "SUM_TO_N", "FIB", "SUCC", "RANGE", "SUM_RANGE",
        "FIZZBUZZ", "MOD", "DIV", "TO_DIGITS", "POW_TWO", "POW_BASE",
    ])
    args = parser.parse_args()
    if args.verify_prefix_profile:
        data = verify_prefix_profile()
        args.output.write_text(json.dumps(data, indent=2) + "\n",
                               encoding="utf-8")
        print(f"Validated full/prefix peak depths in {len(data)} cases")
        return
    if args.stack_prefix and set(args.kinds) - {"FACT", "POW_TWO", "POW_BASE"}:
        parser.error("--stack-prefix supports only FACT, POW_TWO, POW_BASE")
    data = {"python": sys.version, "executable": sys.executable,
            "platform": platform.platform(), "recursion_limit": 1000,
            "stack_prefix": args.stack_prefix,
            "timeout_seconds": args.timeout, "measurements": {}}
    if args.output.exists():
        data["measurements"] = json.loads(
            args.output.read_text(encoding="utf-8"))["measurements"]
    for kind in args.kinds:
        entry = {}
        for mode in ("direct", "doctest"):
            entry[mode] = boundary(kind, mode, args.timeout,
                                   prefix=args.stack_prefix)
            print(kind, mode, json.dumps(entry[mode], ensure_ascii=False),
                  flush=True)
        entry["smaller_completed"] = min(
            entry[mode]["largest_completed"] for mode in ("direct", "doctest"))
        entry["safe_n"] = math.floor(entry["smaller_completed"] * 0.8)
        if kind == "FIB":
            entry["timings"] = {
                str(n): {mode: probe(kind, n, mode, args.timeout)
                         for mode in ("direct", "doctest")}
                for n in range(max(0, entry["smaller_completed"] - 3),
                               entry["smaller_completed"] + 1)
            }
        if kind == "FIZZBUZZ":
            entry["one_to_fifteen"] = {
                mode: probe(kind, 15, mode, args.timeout)
                for mode in ("direct", "doctest")
            }
        if kind == "POW_TWO":
            entry["two_to_ten"] = {
                mode: probe(kind, 10, mode, args.timeout)
                for mode in ("direct", "doctest")
            }
        if kind in {"MOD", "DIV"}:
            n = entry["doctest"]["next_n"]
            entry["boundary_divisors"] = {
                "doctest_n": n,
                "statuses": {str(d): probe(kind, n, "doctest",
                                           args.timeout, d)["status"]
                             for d in range(1, 8)},
            }
        data["measurements"][kind] = entry
        args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2)
                               + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
