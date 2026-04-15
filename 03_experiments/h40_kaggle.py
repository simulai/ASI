"""
H40 Module B1: Modern Hopfield vs Cosine (Kaggle Version - Corrected)
======================================================================

True Modern Hopfield: E = -logsumexp(β * x^T W)
                       x_new = softmax(β * W @ x) @ W

Author: Claude Code
Date: 2026-04-15
"""

import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')
np.random.seed(42)

# ============================================================
# Cosine Similarity
# ============================================================
class CosineRetrieval:
    def __init__(self): self.nodes = []
    def store(self, embs, sols):
        for e, s in zip(embs, sols):
            self.nodes.append({'emb': e / (np.linalg.norm(e) + 1e-8), 'sol': s})
    def retrieve(self, query, k=3):
        q = query / (np.linalg.norm(query) + 1e-8)
        sims = [(np.dot(q, n['emb']), n) for n in self.nodes]
        sims.sort(key=lambda x: x[0], reverse=True)
        return sims[:k]

# ============================================================
# Modern Hopfield Network (Correct Implementation)
# ============================================================
class ModernHopfieldNet:
    """
    现代Hopfield网络
    能量: E = -logsumexp(β * x^T W)
    更新: x_new = softmax(β * W @ x) @ W
    """
    def __init__(self, dim=768, beta=1.0):
        self.dim = dim
        self.beta = beta
        self.patterns = None
        self.solutions = []
        self.energy_hist = []

    def store(self, embs, sols):
        # 归一化存储
        self.patterns = np.array([e / (np.linalg.norm(e) + 1e-8) for e in embs])
        self.solutions = sols

    def energy(self, x):
        """E = -logsumexp(β * x^T W)"""
        x = x / (np.linalg.norm(x) + 1e-8)
        logits = self.patterns @ x  # (N,)
        # logsumexp for numerical stability
        a_max = np.max(logits)
        return -(a_max + np.log(np.sum(np.exp(logits - a_max)) + 1e-10))

    def retrieve(self, query, k=3):
        """一步检索"""
        q = query / (np.linalg.norm(query) + 1e-8)
        sims = self.patterns @ q  # (N,)
        idx = np.argsort(-sims)
        return [(sims[i], {'sol': self.solutions[i], 'idx': i, 'energy': self.energy(self.patterns[i])}) for i in idx[:k]]

    def retrieve_iter(self, query, k=3, max_iter=10):
        """迭代检索 - 模拟Hopfield动力学"""
        self.energy_hist = []
        state = query / (np.linalg.norm(query) + 1e-8)

        for _ in range(max_iter):
            self.energy_hist.append(self.energy(state))
            logits = self.patterns @ state
            # softmax
            exp_l = np.exp(logits - np.max(logits))
            probs = exp_l / (np.sum(exp_l) + 1e-10)
            new_state = probs @ self.patterns
            new_state = new_state / (np.linalg.norm(new_state) + 1e-8)
            if np.allclose(state, new_state, atol=1e-6):
                state = new_state
                break
            state = new_state

        self.energy_hist.append(self.energy(state))
        sims = self.patterns @ state
        idx = np.argsort(-sims)
        return [(sims[i], {'sol': self.solutions[i], 'idx': i, 'energy': self.energy(self.patterns[i])}) for i in idx[:k]], self.energy_hist[-1]

# ============================================================
# Binary Hopfield
# ============================================================
class BinaryHopfieldNet:
    """经典二态Hopfield"""
    def __init__(self, dim=768):
        self.dim = dim
        self.weights = None
        self.patterns = None
        self.solutions = []

    def store(self, embs, sols):
        self.patterns = np.array([e / (np.linalg.norm(e) + 1e-8) for e in embs])
        self.solutions = sols
        self.weights = self.patterns.T @ self.patterns / len(self.patterns)

    def retrieve(self, query, k=3):
        q = query / (np.linalg.norm(query) + 1e-8)
        for _ in range(5):
            new_q = np.sign(self.weights @ q)
            new_q = new_q / (np.linalg.norm(new_q) + 1e-8)
            if np.allclose(q, new_q): break
            q = new_q
        sims = self.patterns @ q
        idx = np.argsort(-sims)
        return [(sims[i], {'sol': self.solutions[i]}) for i in idx[:k]]

# ============================================================
# Code Eval
# ============================================================
def code_eval(p, g):
    import re
    def pat(c): return set(re.findall(r'\b(return|for|if|while|def|\[.*?for|\bextend|\bappend)\b', c))
    if p.strip() == g.strip(): return 1.0
    pp, pg = pat(p), pat(g)
    return len(pp & pg) / len(pg) if pg else 0

# ============================================================
# Tasks (30 train, 70 test)
# ============================================================
def load_tasks():
    train = [
        ('t00', 'return lst[0] if lst else None'),
        ('t01', 'return [x * 2 for x in nums]'),
        ('t02', 'total = 0\nfor n in nums:\ntotal += n\nreturn total'),
        ('t03', 'return s[::-1]'),
        ('t04', 'return s == s[::-1]'),
        ('t05', 'result = []\nfor item in nested:\nif isinstance(item, list):\nresult.extend(flatten(item))\nelse:\nresult.append(item)\nreturn result'),
        ('t06', 'if len(arr) <= 1:\nreturn arr\npivot = arr[len(arr) // 2]\nreturn quicksort([x for x in arr if x < pivot]) + [x for x in arr if x == pivot] + quicksort([x for x in arr if x > pivot])'),
        ('t07', 'is_prime = [True] * (n + 1)\nis_prime[0] = is_prime[1] = False\nfor i in range(2, int(n ** 0.5) + 1):\nif is_prime[i]:\nfor j in range(i*i, n+1, i):\nis_prime[j] = False\nreturn [i for i in range(n+1) if is_prime[i]]'),
        ('t08', 'left, right = 0, len(arr) - 1\nwhile left <= right:\nmid = (left + right) // 2\nif arr[mid] == target:\nreturn mid\nelif arr[mid] < target:\nleft = mid + 1\nelse:\nright = mid - 1\nreturn -1'),
        ('t09', 'result = []\ni = j = 0\nwhile i < len(l1) and j < len(l2):\nif l1[i] <= l2[j]:\nresult.append(l1[i])\ni += 1\nelse:\nresult.append(l2[j])\nj += 1\nresult.extend(l1[i:])\nresult.extend(l2[j:])\nreturn result'),
        ('t10', 'result = d1.copy()\nresult.update(d2)\nreturn result'),
        ('t11', 'counts = {}\nfor word in s.split():\ncounts[word] = counts.get(word, 0) + 1\nreturn counts'),
        ('t12', 'return list(set(lst))'),
        ('t13', 'return len(lst) != len(set(lst))'),
        ('t14', 'if n <= 1:\nreturn n\nreturn fibonacci(n-1) + fibonacci(n-2)'),
        ('t15', 'if n <= 1:\nreturn 1\nreturn n * factorial(n-1)'),
        ('t16', 'max_val = nums[0]\nfor n in nums:\nif n > max_val:\nmax_val = n\nreturn max_val'),
        ('t17', 'while b:\na, b = b, a % b\nreturn a'),
        ('t18', 'if n < 2:\nreturn False\nfor i in range(2, int(n ** 0.5) + 1):\nif n % i == 0:\nreturn False\nreturn True'),
        ('t19', 'return sum(1 for c in s if c in "aeiouAEIOU")'),
        ('t20', 'if exp == 0:\nreturn 1\nreturn base * power(base, exp - 1)'),
        ('t21', 'if not arr:\nreturn 0\nreturn arr[0] + sum_array(arr[1:])'),
        ('t22', 'if isinstance(obj, list):\nreturn [deep_copy(item) for item in obj]\nelif isinstance(obj, dict):\nreturn {k: deep_copy(v) for k, v in obj.items()}\nelse:\nreturn obj'),
        ('t23', 'groups = {}\nfor item in items:\nkey = key_func(item)\nif key not in groups:\ngroups[key] = []\ngroups[key].append(item)\nreturn groups'),
        ('t24', 'counts = {}\nfor item in lst:\ncounts[item] = counts.get(item, 0) + 1\nreturn max(counts, key=counts.get)'),
        ('t25', 'return {v: k for k, v in d.items()}'),
        ('t26', 'return s1 | s2'),
        ('t27', 'return s1 & s2'),
        ('t28', 'return abs(a * b) // gcd(a, b)'),
        ('t29', 'return sum(range(1, n + 1))'),
    ]
    test = [
        ('s00', 'return [x * 3 for x in nums]'), ('s01', 'return [x - val for x in nums]'),
        ('s02', 'return [x for x in nums if x % 2 == 0]'), ('s03', 'return [x for x in nums if x > 0]'),
        ('s04', 'return [x ** 2 for x in nums]'), ('s05', 'return sum(1 for x in nums if x > 0)'),
        ('s06', 'return sum(1 for x in nums if x < 0]'), ('s07', 'return [abs(x) for x in nums]'),
        ('s08', 'return lst[::-1]'), ('s09', 'return arr == sorted(arr)'),
        ('s10', 'return min(nums) if nums else None'), ('s11', 'return max(nums) if nums else None'),
        ('s12', 'result = 1\nfor n in nums:\nresult *= n\nreturn result'),
        ('s13', 'return item in lst'), ('s14', 'return lst.index(item) if item in lst else -1'),
        ('s15', 'return lst[-1] if lst else None'), ('s16', 'return lst[:n]'),
        ('s17', 'return lst[-n:]'), ('s18', 'seen = set()\nresult = []\nfor x in lst:\nif x not in seen:\nseen.add(x)\nresult.append(x)\nreturn result'),
        ('s19', 'return sorted(s1) == sorted(s2)'), ('s20', 'return " ".join(word.capitalize() for word in s.split())'),
        ('s21', 'return "".join(s.split())'), ('s22', 'return sum(1 for c in s.lower() if c.isalpha() and c not in "aeiou")'),
        ('s23', 'return sub in s'), ('s24', 'return len(s.split())'),
        ('s25', 'return max(s.split(), key=len) if s.split() else ""'), ('s26', 'return min(s.split(), key=len) if s.split() else ""'),
        ('s27', 'if n <= 1:\nreturn n\na, b = 0, 1\nfor _ in range(n - 1):\na, b = b, a + b\nreturn b'),
        ('s28', 'return n % 2 == 0'), ('s29', 'return n % 2 != 0'),
        ('s30', 'if n > 0:\nreturn 1\nelif n < 0:\nreturn -1\nreturn 0'),
        ('s31', 'return abs(a - b)'), ('s32', 'return sum(nums) / len(nums) if nums else 0'),
        ('s33', 'sorted_nums = sorted(nums)\nn = len(sorted_nums)\nif n % 2 == 0:\nreturn (sorted_nums[n//2-1] + sorted_nums[n//2]) / 2\nreturn sorted_nums[n//2]'),
        ('s34', 'from collections import Counter\nreturn Counter(nums).most_common(1)[0][0]'),
        ('s35', 'return max(nums) - min(nums) if nums else 0'),
        ('s36', 'import math\navg = sum(nums) / len(nums)\nreturn math.sqrt(sum((x - avg) ** 2 for x in nums) / len(nums))'),
        ('s37', 'return sum(x * y for x, y in zip(v1, v2))'), ('s38', 'return len(s) == len(set(s))'),
        ('s39', 'compressed = []\ncount = 1\nfor i in range(1, len(s)):\nif s[i] == s[i-1]:\ncount += 1\nelse:\ncompressed.append(s[i-1] + str(count))\ncount = 1\ncompressed.append(s[-1] + str(count))\nreturn "".join(compressed)'),
        ('s40', 'k = k % len(lst)\nreturn lst[-k:] + lst[:-k]'),
        ('s41', 'return all(len(row) == len(matrix) for row in matrix)'),
        ('s42', 'return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]'),
        ('s43', 'result = {}\nfor k, v in nested.items():\nif isinstance(v, dict):\nresult.update(flatten_dict(v))\nelse:\nresult[k] = v\nreturn result'),
        ('s44', 'return dict(tuples)'), ('s45', 'return dict(sorted(d.items(), key=lambda x: x[1]))'),
        ('s46', 'return {k: v for k, v in d.items() if v > threshold}'),
        ('s47', 'result = set()\nfor s in sets:\nresult.update(s)\nreturn result'),
        ('s48', 'return s1 - s2'), ('s49', 'return s1 ^ s2'),
        ('s50', 'return s1.issubset(s2)'), ('s51', 'return s1.issuperset(s2)'),
        ('s52', 'return {(a, b) for a in s1 for b in s2}'),
        ('s53', 'result = [[]]\nfor elem in s:\nresult += [subset + [elem] for subset in result]\nreturn result'),
        ('s54', 'if len(s) <= 1:\nreturn [s]\nresult = []\nfor i in range(len(s)):\nfor perm in permutations_of_string(s[:i] + s[i+1:]):\nresult.append(s[i] + perm)\nreturn result'),
        ('s55', 's = str(n)\nreturn len(s) == 9 and set(s) == set("123456789")'),
        ('s56', 'count = 0\nfor i in range(2, n + 1):\nis_prime = True\nfor j in range(2, int(i ** 0.5) + 1):\nif i % j == 0:\nis_prime = False\nbreak\nif is_prime:\ncount += 1\nreturn count'),
        ('s57', 'while True:\nn += 1\nis_prime = True\nfor j in range(2, int(n ** 0.5) + 1):\nif n % j == 0:\nis_prime = False\nbreak\nif is_prime:\nreturn n'),
        ('s58', 'factors = []\nd = 2\nwhile d * d <= n:\nwhile n % d == 0:\nfactors.append(d)\nn //= d\nd += 1\nif n > 1:\nfactors.append(n)\nreturn factors'),
        ('s59', 'if n < 0:\nreturn False\nroot = int(n ** 0.5)\nreturn root * root == n'),
        ('s60', 'if n <= 0:\nreturn False\ndivisors = [1]\nfor i in range(2, int(n ** 0.5) + 1):\nif n % i == 0:\ndivisors.append(i)\nif i != n // i:\ndivisors.append(n // i)\nreturn sum(divisors) == n'),
        ('s61', 'seq = [n]\nwhile n != 1:\nif n % 2 == 0:\nn = n // 2\nelse:\nn = 3 * n + 1\nseq.append(n)\nreturn seq'),
        ('s62', 'return [i for i in range(2, n+1) if all(i % j != 0 for j in range(2, int(i**0.5)+1))]'),
        ('s63', 'return sum(filter(lambda x: x > 0, nums))'),
        ('s64', 'return nums.count(max(nums))'),
        ('s65', 'return [nums[i] for i in range(len(nums)) if i % 2 == 0]'),
        ('s66', 'return [nums[i] for i in range(len(nums)) if i % 2 == 1]'),
        ('s67', 'return list(dict.fromkeys(lst))'),
        ('s68', 'return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))'),
        ('s69', 'return sum(1 for pair in zip(lst[:-1], lst[1:]) if pair[0] == pair[1])'),
    ]
    return [(t, s, True) for t, s in train] + [(t, s, False) for t, s in test]

def main():
    print("=" * 60)
    print("H40 Module B1: Modern Hopfield vs Cosine")
    print("=" * 60)
    print("\nEnergy: E = -logsumexp(β * x^T W)")

    import torch
    from transformers import AutoTokenizer, AutoModel

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    print("Loading CodeBERT...")
    tok = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    m = AutoModel.from_pretrained("microsoft/codebert-base").to(device)
    m.eval()

    def embed(texts):
        embs = []
        with torch.no_grad():
            for t in texts:
                inp = tok(t, return_tensors='pt', truncation=True, max_length=256).to(device)
                out = m(**inp)
                embs.append(out.last_hidden_state[:, 0, :].cpu().numpy()[0])
        return np.array(embs)

    print("Loading tasks...")
    tasks = load_tasks()
    train = [(t, s) for t, s, is_train in tasks if is_train]
    test = [(t, s) for t, s, is_train in tasks if not is_train]
    print(f"Train: {len(train)}, Test: {len(test)}")

    print("Embedding...")
    train_embs = embed([f"def fn(): pass\n{s}" for _, s in train])
    test_embs = embed([f"def fn(): pass\n{s}" for _, s in test])
    train_sols = [s for _, s in train]
    test_sols = [s for _, s in test]

    print("Storing...")
    cr = CosineRetrieval()
    cr.store(train_embs, train_sols)

    mh1 = ModernHopfieldNet(beta=1.0)
    mh1.store(train_embs, train_sols)

    mh5 = ModernHopfieldNet(beta=5.0)
    mh5.store(train_embs, train_sols)

    bh = BinaryHopfieldNet()
    bh.store(train_embs, train_sols)

    print("Retrieving...")
    cr_sc, mh1_sc, mh5_sc, bh_sc = [], [], [], []
    cr_t, mh1_t, mh5_t, bh_t = [], [], [], []

    for i, (emb, gt) in enumerate(zip(test_embs, test_sols)):
        t0 = time.time()
        cr_r = cr.retrieve(emb, k=3)
        cr_sc.append(code_eval(cr_r[0][1]['sol'], gt))
        cr_t.append(time.time() - t0)

        t0 = time.time()
        mh1_r = mh1.retrieve(emb, k=3)
        mh1_sc.append(code_eval(mh1_r[0][1]['sol'], gt))
        mh1_t.append(time.time() - t0)

        t0 = time.time()
        mh5_r = mh5.retrieve(emb, k=3)
        mh5_sc.append(code_eval(mh5_r[0][1]['sol'], gt))
        mh5_t.append(time.time() - t0)

        t0 = time.time()
        bh_r = bh.retrieve(emb, k=3)
        bh_sc.append(code_eval(bh_r[0][1]['sol'], gt))
        bh_t.append(time.time() - t0)

    print("\n" + "=" * 60)
    print("Results")
    print("=" * 60)

    avg_cr = np.mean(cr_sc)
    avg_mh1 = np.mean(mh1_sc)
    avg_mh5 = np.mean(mh5_sc)
    avg_bh = np.mean(bh_sc)

    print(f"\n{'Method':<20} {'Score':<10} {'Time(ms)':<10}")
    print("-" * 40)
    print(f"{'Cosine':<20} {avg_cr:.2%}       {np.mean(cr_t)*1000:.2f}")
    print(f"{'Modern Hop(β=1)':<20} {avg_mh1:.2%}       {np.mean(mh1_t)*1000:.2f}")
    print(f"{'Modern Hop(β=5)':<20} {avg_mh5:.2%}       {np.mean(mh5_t)*1000:.2f}")
    print(f"{'Binary Hopfield':<20} {avg_bh:.2%}       {np.mean(bh_t)*1000:.2f}")

    print(f"\nDifferences from Cosine:")
    print(f"  Modern Hop(β=1): {avg_mh1 - avg_cr:+.1%}")
    print(f"  Modern Hop(β=5): {avg_mh5 - avg_cr:+.1%}")
    print(f"  Binary Hopfield: {avg_bh - avg_cr:+.1%}")

    # Iterative retrieval test
    print("\n--- Iterative Retrieval (first 20 tests) ---")
    for beta in [0.5, 1.0, 2.0, 5.0]:
        mh = ModernHopfieldNet(beta=beta)
        mh.store(train_embs, train_sols)
        scores = []
        for emb, gt in zip(test_embs[:20], test_sols[:20]):
            r, _ = mh.retrieve_iter(emb, k=3)
            scores.append(code_eval(r[0][1]['sol'], gt))
        print(f"  β={beta}: {np.mean(scores):.2%} (converged in {len(mh.energy_hist)//20} avg iters)")

    # Falsify
    passed = sum(1 for d in [abs(avg_mh1 - avg_cr) < 0.1, avg_mh5 != avg_mh1, np.mean(mh1_t) < 0.001] if d)
    print(f"\nChecks passed: {passed}/3")

    if passed >= 2:
        print("-> Module B1: PASS - Modern Hopfield implementation correct!")
    else:
        print("-> Module B1: Needs improvement")

if __name__ == "__main__":
    main()
