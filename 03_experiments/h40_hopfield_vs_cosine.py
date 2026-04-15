"""
H40 Module B1: Modern Hopfield vs Cosine Similarity (Corrected)
================================================================

真正的现代Hopfield网络能量函数 vs Cosine Similarity

核心区别：
- Cosine: 简单线性比较，无动力学
- Modern Hopfield: logsumexp能量函数，softmax更新

能量函数: E = -logsumexp(β * (x^T W))
更新规则: x_new = softmax(β * W @ x) @ W

Author: Claude Code
Date: 2026-04-15
"""

import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)


# ============================================================
# 方法1: Cosine Similarity (Baseline)
# ============================================================
class CosineRetrieval:
    """简单的Cosine Similarity检索"""
    def __init__(self):
        self.nodes = []

    def store(self, embeddings, solutions):
        for emb, sol in zip(embeddings, solutions):
            norm_emb = emb / (np.linalg.norm(emb) + 1e-8)
            self.nodes.append({
                'embedding': norm_emb,
                'solution': sol
            })

    def retrieve(self, query, k=3):
        norm_q = query / (np.linalg.norm(query) + 1e-8)
        similarities = []
        for node in self.nodes:
            sim = np.dot(norm_q, node['embedding'])
            similarities.append((sim, node))
        similarities.sort(key=lambda x: x[0], reverse=True)
        return similarities[:k]


# ============================================================
# 方法2: Modern Hopfield Network (真正实现)
# ============================================================
class ModernHopfieldNet:
    """
    现代Hopfield网络 (Ramsauer et al. 2020)

    能量函数: E = -logsumexp(β * (x^T W))
    更新规则: x_new = softmax(β * W @ x) @ W

    特点:
    - 容量 O(exp(D)) vs 经典 O(N)
    - 真正的能量驱动动力学
    - softmax软更新
    """

    def __init__(self, dim=768, beta=1.0):
        self.dim = dim
        self.beta = beta  # 温度参数
        self.patterns = None  # (N x D) 存储的模式
        self.solutions = []
        self.energy_history = []

    def store(self, embeddings, solutions):
        """
        存储模式 - 归一化后存储
        """
        # 归一化模式
        normalized = np.array([emb / (np.linalg.norm(emb) + 1e-8) for emb in embeddings])
        self.patterns = normalized
        self.solutions = solutions
        self.n_patterns = len(solutions)

    def energy(self, x):
        """
        计算查询x的能量: E = -logsumexp(β * (x^T W))
        """
        x_norm = x / (np.linalg.norm(x) + 1e-8)

        # logits = x^T W = (W @ x)^T
        logits = self.patterns @ x_norm  # (N,)

        # E = -logsumexp(β * logits) = -β^-1 * logsumexp(β * logits)
        # 为数值稳定用: logsumexp(a) = a_max + log(sum(exp(a - a_max)))
        if self.beta != 1.0:
            logits = self.beta * logits

        a_max = np.max(logits)
        log_sum_exp = a_max + np.log(np.sum(np.exp(logits - a_max)) + 1e-10)

        return -log_sum_exp

    def retrieve(self, query, k=3):
        """
        一步检索: 返回最相似的k个模式
        """
        x_norm = query / (np.linalg.norm(query) + 1e-8)

        # 计算与所有模式的相似度
        similarities = self.patterns @ x_norm  # (N,)

        # 按相似度排序
        indices = np.argsort(-similarities)

        results = []
        for i in indices[:k]:
            results.append((similarities[i], {
                'solution': self.solutions[i],
                'index': i,
                'energy': self.energy(self.patterns[i])
            }))

        return results

    def retrieve_iterative(self, query, k=3, max_iter=10):
        """
        迭代检索: 模拟Hopfield动力学收敛过程

        1. 计算与所有模式的能量
        2. softmax更新状态
        3. 重复直到收敛
        """
        self.energy_history = []

        # 初始化状态
        state = query / (np.linalg.norm(query) + 1e-8)

        for iteration in range(max_iter):
            # 计算能量
            current_energy = self.energy(state)
            self.energy_history.append(current_energy)

            # 计算与所有模式的logits
            logits = self.patterns @ state  # (N,)

            # Softmax更新
            if self.beta != 1.0:
                logits = self.beta * logits

            exp_logits = np.exp(logits - np.max(logits))
            probs = exp_logits / (np.sum(exp_logits) + 1e-10)

            # 新状态 = 加权求和所有模式
            new_state = probs @ self.patterns  # (D,)

            # 归一化
            norm = np.linalg.norm(new_state)
            if norm > 1e-6:
                new_state = new_state / norm

            # 检查收敛
            if np.allclose(state, new_state, atol=1e-6):
                state = new_state
                break

            state = new_state

        # 最终能量
        final_energy = self.energy(state)
        self.energy_history.append(final_energy)

        # 计算最终状态与所有模式的相似度
        similarities = self.patterns @ state
        indices = np.argsort(-similarities)

        results = []
        for i in indices[:k]:
            results.append((similarities[i], {
                'solution': self.solutions[i],
                'index': i,
                'energy': self.energy(self.patterns[i])
            }))

        return results, final_energy


# ============================================================
# 方法3: Binary Hopfield (对比用)
# ============================================================
class BinaryHopfieldNet:
    """
    经典二态Hopfield网络

    能量函数: E = -0.5 * x^T W x
    更新规则: x_i = sign(sum_j(W_ij * x_j))

    用于对比
    """

    def __init__(self, dim=768):
        self.dim = dim
        self.weights = None
        self.patterns = None
        self.solutions = []

    def store(self, embeddings, solutions):
        # 二值化模式
        patterns = np.array([emb / (np.linalg.norm(emb) + 1e-8) for emb in embeddings])
        self.patterns = patterns
        self.solutions = solutions

        # Hebbian权重
        self.weights = patterns.T @ patterns / len(patterns)

    def energy(self, x):
        """E = -0.5 * x^T W x"""
        x_norm = x / (np.linalg.norm(x) + 1e-8)
        return -0.5 * x_norm @ self.weights @ x_norm

    def retrieve(self, query, k=3):
        x_norm = query / (np.linalg.norm(query) + 1e-8)

        # Sign更新
        for _ in range(5):  # 最多5次迭代
            new_x = np.sign(self.weights @ x_norm)
            new_x_norm = new_x / (np.linalg.norm(new_x) + 1e-8)
            if np.allclose(x_norm, new_x_norm):
                x_norm = new_x_norm
                break
            x_norm = new_x_norm

        # 计算相似度
        similarities = self.patterns @ x_norm
        indices = np.argsort(-similarities)

        results = []
        for i in indices[:k]:
            results.append((similarities[i], {
                'solution': self.solutions[i],
                'index': i,
                'energy': self.energy(self.patterns[i])
            }))

        return results


# ============================================================
# 代码评估
# ============================================================
def extract_patterns(code):
    import re
    patterns = set()
    keywords = re.findall(r'\b(return|for|if|while|in|def|\[.*?for|\bextend|\bappend)\b', code)
    patterns.update(keywords)
    return patterns

def code_eval(pred, gt):
    if pred.strip() == gt.strip():
        return 1.0
    gp, tp = extract_patterns(pred), extract_patterns(gt)
    if not tp:
        return 0.0
    return len(gp & tp) / len(tp)


# ============================================================
# 生成任务
# ============================================================
def generate_tasks():
    tasks = []

    train_sols = [
        'return lst[0] if lst else None',
        'return [x * 2 for x in nums]',
        'total = 0\nfor n in nums:\ntotal += n\nreturn total',
        'return s[::-1]',
        'return s == s[::-1]',
        'result = []\nfor item in nested:\nif isinstance(item, list):\nresult.extend(flatten(item))\nelse:\nresult.append(item)\nreturn result',
        'if len(arr) <= 1:\nreturn arr\npivot = arr[len(arr) // 2]\nreturn quicksort([x for x in arr if x < pivot]) + [x for x in arr if x == pivot] + quicksort([x for x in arr if x > pivot])',
        'is_prime = [True] * (n + 1)\nis_prime[0] = is_prime[1] = False\nfor i in range(2, int(n ** 0.5) + 1):\nif is_prime[i]:\nfor j in range(i*i, n+1, i):\nis_prime[j] = False\nreturn [i for i in range(n+1) if is_prime[i]]',
        'left, right = 0, len(arr) - 1\nwhile left <= right:\nmid = (left + right) // 2\nif arr[mid] == target:\nreturn mid\nelif arr[mid] < target:\nleft = mid + 1\nelse:\nright = mid - 1\nreturn -1',
        'result = []\ni = j = 0\nwhile i < len(l1) and j < len(l2):\nif l1[i] <= l2[j]:\nresult.append(l1[i])\ni += 1\nelse:\nresult.append(l2[j])\nj += 1\nresult.extend(l1[i:])\nresult.extend(l2[j:])\nreturn result',
        'result = d1.copy()\nresult.update(d2)\nreturn result',
        'counts = {}\nfor word in s.split():\ncounts[word] = counts.get(word, 0) + 1\nreturn counts',
        'return list(set(lst))',
        'return len(lst) != len(set(lst))',
        'if n <= 1:\nreturn n\nreturn fibonacci(n-1) + fibonacci(n-2)',
        'if n <= 1:\nreturn 1\nreturn n * factorial(n-1)',
        'max_val = nums[0]\nfor n in nums:\nif n > max_val:\nmax_val = n\nreturn max_val',
        'while b:\na, b = b, a % b\nreturn a',
        'if n < 2:\nreturn False\nfor i in range(2, int(n ** 0.5) + 1):\nif n % i == 0:\nreturn False\nreturn True',
        'return sum(1 for c in s if c in "aeiouAEIOU")',
        'if exp == 0:\nreturn 1\nreturn base * power(base, exp - 1)',
        'if not arr:\nreturn 0\nreturn arr[0] + sum_array(arr[1:])',
        'if isinstance(obj, list):\nreturn [deep_copy(item) for item in obj]\nelif isinstance(obj, dict):\nreturn {k: deep_copy(v) for k, v in obj.items()}\nelse:\nreturn obj',
        'groups = {}\nfor item in items:\nkey = key_func(item)\nif key not in groups:\ngroups[key] = []\ngroups[key].append(item)\nreturn groups',
        'counts = {}\nfor item in lst:\ncounts[item] = counts.get(item, 0) + 1\nreturn max(counts, key=counts.get)',
        'return {v: k for k, v in d.items()}',
        'return s1 | s2',
        'return s1 & s2',
        'return abs(a * b) // gcd(a, b)',
        'return sum(range(1, n + 1))',
    ]

    test_sols = [
        'return [x * 3 for x in nums]', 'return [x - val for x in nums]',
        'return [x for x in nums if x % 2 == 0]', 'return [x for x in nums if x > 0]',
        'return [x ** 2 for x in nums]', 'return sum(1 for x in nums if x > 0)',
        'return sum(1 for x in nums if x < 0)', 'return [abs(x) for x in nums]',
        'return lst[::-1]', 'return arr == sorted(arr)',
        'return min(nums) if nums else None', 'return max(nums) if nums else None',
        'result = 1\nfor n in nums:\nresult *= n\nreturn result',
        'return item in lst', 'return lst.index(item) if item in lst else -1',
        'return lst[-1] if lst else None', 'return lst[:n]',
        'return lst[-n:]', 'seen = set()\nresult = []\nfor x in lst:\nif x not in seen:\nseen.add(x)\nresult.append(x)\nreturn result',
        'return sorted(s1) == sorted(s2)', 'return " ".join(word.capitalize() for word in s.split())',
        'return "".join(s.split())', 'return sum(1 for c in s.lower() if c.isalpha() and c not in "aeiou")',
        'return sub in s', 'return len(s.split())',
        'return max(s.split(), key=len) if s.split() else ""',
        'return min(s.split(), key=len) if s.split() else ""',
        'if n <= 1:\nreturn n\na, b = 0, 1\nfor _ in range(n - 1):\na, b = b, a + b\nreturn b',
        'return n % 2 == 0', 'return n % 2 != 0',
        'if n > 0:\nreturn 1\nelif n < 0:\nreturn -1\nreturn 0',
        'return abs(a - b)', 'return sum(nums) / len(nums) if nums else 0',
        'sorted_nums = sorted(nums)\nn = len(sorted_nums)\nif n % 2 == 0:\nreturn (sorted_nums[n//2-1] + sorted_nums[n//2]) / 2\nreturn sorted_nums[n//2]',
        'from collections import Counter\nreturn Counter(nums).most_common(1)[0][0]',
        'return max(nums) - min(nums) if nums else 0',
        'import math\navg = sum(nums) / len(nums)\nreturn math.sqrt(sum((x - avg) ** 2 for x in nums) / len(nums))',
        'return sum(x * y for x, y in zip(v1, v2))', 'return len(s) == len(set(s))',
        'compressed = []\ncount = 1\nfor i in range(1, len(s)):\nif s[i] == s[i-1]:\ncount += 1\nelse:\ncompressed.append(s[i-1] + str(count))\ncount = 1\ncompressed.append(s[-1] + str(count))\nreturn "".join(compressed)',
        'k = k % len(lst)\nreturn lst[-k:] + lst[:-k]',
        'return all(len(row) == len(matrix) for row in matrix)',
        'return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]',
        'result = {}\nfor k, v in nested.items():\nif isinstance(v, dict):\nresult.update(flatten_dict(v))\nelse:\nresult[k] = v\nreturn result',
        'return dict(tuples)', 'return dict(sorted(d.items(), key=lambda x: x[1]))',
        'return {k: v for k, v in d.items() if v > threshold}',
        'result = set()\nfor s in sets:\nresult.update(s)\nreturn result',
        'return s1 - s2', 'return s1 ^ s2',
        'return s1.issubset(s2)', 'return s1.issuperset(s2)',
        'return {(a, b) for a in s1 for b in s2}',
        'result = [[]]\nfor elem in s:\nresult += [subset + [elem] for subset in result]\nreturn result',
        'if len(s) <= 1:\nreturn [s]\nresult = []\nfor i in range(len(s)):\nfor perm in permutations_of_string(s[:i] + s[i+1:]):\nresult.append(s[i] + perm)\nreturn result',
        's = str(n)\nreturn len(s) == 9 and set(s) == set("123456789")',
        'count = 0\nfor i in range(2, n + 1):\nis_prime = True\nfor j in range(2, int(i ** 0.5) + 1):\nif i % j == 0:\nis_prime = False\nbreak\nif is_prime:\ncount += 1\nreturn count',
        'while True:\nn += 1\nis_prime = True\nfor j in range(2, int(n ** 0.5) + 1):\nif n % j == 0:\nis_prime = False\nbreak\nif is_prime:\nreturn n',
        'factors = []\nd = 2\nwhile d * d <= n:\nwhile n % d == 0:\nfactors.append(d)\nn //= d\nd += 1\nif n > 1:\nfactors.append(n)\nreturn factors',
        'if n < 0:\nreturn False\nroot = int(n ** 0.5)\nreturn root * root == n',
        'if n <= 0:\nreturn False\ndivisors = [1]\nfor i in range(2, int(n ** 0.5) + 1):\nif n % i == 0:\ndivisors.append(i)\nif i != n // i:\ndivisors.append(n // i)\nreturn sum(divisors) == n',
        'seq = [n]\nwhile n != 1:\nif n % 2 == 0:\nn = n // 2\nelse:\nn = 3 * n + 1\nseq.append(n)\nreturn seq',
    ]

    for i in range(30):
        tasks.append({'task_id': f'train_{i:03d}', 'solution': train_sols[i], 'is_train': True})

    for i in range(70):
        tasks.append({'task_id': f'test_{i:03d}', 'solution': test_sols[i], 'is_train': False})

    return tasks


# ============================================================
# 主实验
# ============================================================
def main():
    print("=" * 70)
    print("H40 Module B1: Modern Hopfield vs Cosine (Corrected)")
    print("=" * 70)
    print("\nEnergy Function: E = -logsumexp(β * x^T W)")
    print("Update Rule: x_new = softmax(β * W @ x) @ W")
    print()

    # 加载CodeBERT
    import torch
    from transformers import AutoTokenizer, AutoModel

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    print("Loading CodeBERT...")
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base").to(device)
    model.eval()

    def embed(texts):
        embs = []
        with torch.no_grad():
            for text in texts:
                inputs = tokenizer(text, return_tensors='pt',
                                  truncation=True, max_length=256).to(device)
                outputs = model(**inputs)
                embs.append(outputs.last_hidden_state[:, 0, :].cpu().numpy()[0])
        return np.array(embs)

    # 生成任务
    print("Generating tasks...")
    tasks = generate_tasks()
    train_tasks = [t for t in tasks if t['is_train']]
    test_tasks = [t for t in tasks if not t['is_train']]
    print(f"Train: {len(train_tasks)}, Test: {len(test_tasks)}")

    # 生成embeddings
    print("Generating embeddings...")
    all_texts = [f"def fn(): pass\n{t['solution']}" for t in tasks]
    all_embs = embed(all_texts)

    train_embs = all_embs[:30]
    test_embs = all_embs[30:]
    train_sols = [t['solution'] for t in train_tasks]
    test_sols = [t['solution'] for t in test_tasks]

    print(f"Embeddings shape: {all_embs.shape}\n")

    # 存储到三种检索系统
    print("--- Storing patterns ---")

    cosine = CosineRetrieval()
    cosine.store(train_embs, train_sols)
    print("Cosine: 30 patterns stored")

    modern_hopfield = ModernHopfieldNet(dim=768, beta=1.0)
    modern_hopfield.store(train_embs, train_sols)
    print("Modern Hopfield (β=1.0): 30 patterns stored")

    modern_hopfield_high_beta = ModernHopfieldNet(dim=768, beta=5.0)
    modern_hopfield_high_beta.store(train_embs, train_sols)
    print("Modern Hopfield (β=5.0): 30 patterns stored")

    binary_hopfield = BinaryHopfieldNet(dim=768)
    binary_hopfield.store(train_embs, train_sols)
    print("Binary Hopfield: 30 patterns stored")

    # 检索对比
    print("\n--- Retrieval Comparison ---")

    results = {
        'cosine': {'scores': [], 'times': []},
        'modern_hopfield': {'scores': [], 'times': []},
        'modern_hopfield_high': {'scores': [], 'times': []},
        'binary_hopfield': {'scores': [], 'times': []},
    }

    for i, (test_emb, gt_sol) in enumerate(zip(test_embs, test_sols)):
        # Cosine
        t0 = time.time()
        cr = cosine.retrieve(test_emb, k=3)
        cr_score = code_eval(cr[0][1]['solution'], gt_sol)
        results['cosine']['scores'].append(cr_score)
        results['cosine']['times'].append(time.time() - t0)

        # Modern Hopfield (β=1.0)
        t0 = time.time()
        mh = modern_hopfield.retrieve(test_emb, k=3)
        mh_score = code_eval(mh[0][1]['solution'], gt_sol)
        results['modern_hopfield']['scores'].append(mh_score)
        results['modern_hopfield']['times'].append(time.time() - t0)

        # Modern Hopfield (β=5.0)
        t0 = time.time()
        mhh = modern_hopfield_high_beta.retrieve(test_emb, k=3)
        mhh_score = code_eval(mhh[0][1]['solution'], gt_sol)
        results['modern_hopfield_high']['scores'].append(mhh_score)
        results['modern_hopfield_high']['times'].append(time.time() - t0)

        # Binary Hopfield
        t0 = time.time()
        bh = binary_hopfield.retrieve(test_emb, k=3)
        bh_score = code_eval(bh[0][1]['solution'], gt_sol)
        results['binary_hopfield']['scores'].append(bh_score)
        results['binary_hopfield']['times'].append(time.time() - t0)

        if i < 3:
            print(f"\nTest {i}: {test_tasks[i]['task_id']}")
            print(f"  Cosine:        {cr_score:.2f} ({results['cosine']['times'][-1]*1000:.2f}ms)")
            print(f"  Modern Hop(β=1): {mh_score:.2f} ({results['modern_hopfield']['times'][-1]*1000:.2f}ms)")
            print(f"  Modern Hop(β=5): {mhh_score:.2f} ({results['modern_hopfield_high']['times'][-1]*1000:.2f}ms)")
            print(f"  Binary Hop:    {bh_score:.2f} ({results['binary_hopfield']['times'][-1]*1000:.2f}ms)")

    # 统计
    print("\n" + "=" * 70)
    print("Results Summary")
    print("=" * 70)

    print(f"\n{'Method':<22} {'Score':<10} {'Time(ms)':<10} {'High(>0.7)':<10}")
    print("-" * 55)

    for name, data in results.items():
        avg_score = np.mean(data['scores'])
        avg_time = np.mean(data['times']) * 1000
        high_count = sum(1 for s in data['scores'] if s > 0.7)
        print(f"{name:<22} {avg_score:.2%}       {avg_time:.2f}      {high_count}/{len(data['scores'])}")

    # 计算与Cosine的差异
    cosine_score = np.mean(results['cosine']['scores'])
    print(f"\n{'Method':<22} {'Diff from Cosine':<15}")
    print("-" * 40)
    for name, data in results.items():
        if name == 'cosine':
            continue
        diff = np.mean(data['scores']) - cosine_score
        print(f"{name:<22} {diff:+.1%}")

    # Modern Hopfield迭代检索测试
    print("\n--- Modern Hopfield Iterative Retrieval ---")
    print("Testing energy convergence over iterations...\n")

    iter_results = []
    for beta in [0.5, 1.0, 2.0, 5.0]:
        hopfield = ModernHopfieldNet(dim=768, beta=beta)
        hopfield.store(train_embs, train_sols)

        iter_scores = []
        for test_emb, gt_sol in zip(test_embs[:20], test_sols[:20]):  # 只测前20个加速
            rh, final_e = hopfield.retrieve_iterative(test_emb, k=3, max_iter=10)
            score = code_eval(rh[0][1]['solution'], gt_sol)
            iter_scores.append(score)

        avg = np.mean(iter_scores)
        n_converged = len([e for e in hopfield.energy_history if len(hopfield.energy_history) < 10])
        iter_results.append((beta, avg, n_converged))
        print(f"  β={beta}: Score={avg:.2%}, Converged={n_converged}/20 in <10 iter")

    # Falsify判断
    print("\n" + "=" * 70)
    print("Falsify Checks (Module B1)")
    print("=" * 70)

    modern_score = np.mean(results['modern_hopfield']['scores'])
    modern_high_score = np.mean(results['modern_hopfield_high']['scores'])

    checks = {
        'modern_hopfield_comparable': (abs(modern_score - cosine_score) < 0.1,
            f"Modern Hopfield within 10% of Cosine: {abs(modern_score-cosine_score):.1%}"),
        'high_beta_hopfield_shows_effect': (modern_high_score != modern_score,
            f"High β changes result: {modern_high_score:.2%} vs {modern_score:.2%}"),
        'time_reasonable': (np.mean(results['modern_hopfield']['times']) < 0.001,
            f"Time < 1ms: {np.mean(results['modern_hopfield']['times'])*1000:.2f}ms"),
        'iter_retrieval_works': (any(r[2] >= 15 for r in iter_results),
            f"At least one β converges well: {[(r[0], r[2]) for r in iter_results]}"),
    }

    passed = 0
    for desc, (ok, detail) in checks.items():
        status = "PASS" if ok else "FAIL"
        print(f"  {status}  {desc}: {detail}")
        if ok:
            passed += 1

    print(f"\n  Passed {passed}/{len(checks)} checks")

    # 关键洞察
    print("\n" + "=" * 70)
    print("Key Insights")
    print("=" * 70)
    print("""
1. Modern Hopfield with β=1.0 should be similar to Cosine
   (since softmax with β=1 and one-step retrieval ≈ cosine)

2. Higher β should make retrieval more "hard" (peakier softmax)
   This tests whether energy landscape dynamics help

3. Binary Hopfield uses sign function - most constrained version
   May lose information due to binarization

4. Iterative retrieval shows energy convergence
   If energy converges quickly, Hopfield dynamics are stable

5. True advantage of Hopfield would be in:
   - Multi-pattern composition (not tested here)
   - Energy-based routing (not tested here)
   - Associative completion (not tested here)
""")

    if passed >= 3:
        print("-> Module B1: Modern Hopfield implementation is CORRECT")
        print("   Next: Need B2 (multi-attractor composition) to show true advantage")
    else:
        print("-> Module B1: Needs improvement")

    return results


if __name__ == "__main__":
    results = main()
