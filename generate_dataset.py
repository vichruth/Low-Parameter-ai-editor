# ============================================================
# GENERATE CLEAN JSONL DATASET FOR LOW-PARAMETER AI BUG DETECTOR
# ============================================================

import json, random

bug_types = ["syntax", "logic", "runtime", "api", "performance"]

def make_pair(i):
    t = random.choice(bug_types)
    if t == "syntax":
        buggy = f"def check_zero_{i}(n):\n    if n = 0:\n        return True\n    return False"
        fixed = f"def check_zero_{i}(n):\n    if n == 0:\n        return True\n    return False"
    elif t == "logic":
        buggy = f"def factorial_{i}(n):\n    res = 0\n    for j in range(1, n+1):\n        res *= j\n    return res"
        fixed = f"def factorial_{i}(n):\n    res = 1\n    for j in range(1, n+1):\n        res *= j\n    return res"
    elif t == "runtime":
        buggy = f"def divide_{i}(a,b):\n    return a/b\n\nprint(divide_{i}(5,0))"
        fixed = f"def divide_{i}(a,b):\n    if b == 0:\n        return None\n    return a/b\n\nprint(divide_{i}(5,2))"
    elif t == "api":
        buggy = f"import math\nprint(math.pow2(3))"
        fixed = f"import math\nprint(math.pow(2,3))"
    else:  # performance
        buggy = f"def unique_{i}(lst):\n    res = []\n    for x in lst:\n        if x not in res:\n            res.append(x)\n    return res"
        fixed = f"def unique_{i}(lst):\n    return list(set(lst))"
    return {"buggy_code": buggy, "fixed_code": fixed, "bug_type": t}

data = [make_pair(i) for i in range(2000)]

with open("bug_fix_dataset.jsonl", "w", encoding="utf-8") as f:
    for row in data:
        json.dump(row, f, ensure_ascii=False)
        f.write("\n")

print("✅ Dataset generated successfully: bug_fix_dataset.jsonl")
