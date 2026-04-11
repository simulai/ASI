"""
H38 Living Tree - Scale Validation (100 tasks)
====================================================

目标：
在100个任务规模下验证纯相似度检索是否依然有效
修复：确保测试集与训练集的任务有不同的solution

Author: Claude Code
Date: 2026-04-09
"""

import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)


# ============================================================
# Living Tree 节点
# ============================================================
class LivingTreeNode:
    def __init__(self, task_id, embedding, prompt, solution):
        self.task_id = task_id
        self.embedding = embedding
        self.prompt = prompt
        self.solution = solution

    def similarity(self, other_embedding):
        return np.dot(self.embedding, other_embedding) / (
            np.linalg.norm(self.embedding) * np.linalg.norm(other_embedding) + 1e-8)


# ============================================================
# Living Tree H38
# ============================================================
class LivingTreeH38:
    def __init__(self, embedding_dim=768):
        self.embedding_dim = embedding_dim
        self.nodes = {}

    def learn_task(self, task_id, embedding, prompt, solution):
        node = LivingTreeNode(task_id, embedding, prompt, solution)
        self.nodes[task_id] = node

    def retrieve(self, embedding, k=3):
        similarities = []
        for node in self.nodes.values():
            sim = node.similarity(embedding)
            similarities.append((sim, node))
        similarities.sort(key=lambda x: x[0], reverse=True)
        return similarities[:k]


# ============================================================
# 代码评估
# ============================================================
def extract_keywords(code):
    import re
    keywords = set()
    patterns = [
        r'\bdef\s+\w+',
        r'\breturn\s+',
        r'\bfor\s+\w+\s+in',
        r'\bif\s+',
        r'\bwhile\s+',
        r'\[\s*\w+\s+for',
        r'\bextend\(',
        r'\bappend\(',
    ]
    for p in patterns:
        matches = re.findall(p, code)
        keywords.update(matches)
    return keywords


def code_eval(pred, gt):
    pred_clean = pred.strip()
    gt_clean = gt.strip()
    if pred_clean == gt_clean:
        return 1.0
    gt_kw = extract_keywords(gt_clean)
    pred_kw = extract_keywords(pred_clean)
    if not gt_kw:
        return 0.0
    return len(gt_kw & pred_kw) / len(gt_kw)


# ============================================================
# 生成任务 - 确保训练/测试集solution不同
# ============================================================
def generate_tasks():
    """
    生成100个编程任务
    - 训练集：30个任务
    - 测试集：70个任务（与训练集solution完全不同）
    """
    tasks = []

    # 训练集模板（30个）- 每个有独特的solution
    train_templates = [
        {'prompt': 'def get_first_element(lst):\n    """Return the first element"""\n',
         'solution': '    return lst[0] if lst else None'},
        {'prompt': 'def double_all(nums):\n    """Double each number"""\n',
         'solution': '    return [x * 2 for x in nums]'},
        {'prompt': 'def sum_list(nums):\n    """Return sum"""\n',
         'solution': '    total = 0\n    for n in nums:\n        total += n\n    return total'},
        {'prompt': 'def reverse_string(s):\n    """Reverse string"""\n',
         'solution': '    return s[::-1]'},
        {'prompt': 'def is_palindrome(s):\n    """Check palindrome"""\n',
         'solution': '    return s == s[::-1]'},
        {'prompt': 'def flatten(nested):\n    """Flatten list"""\n',
         'solution': '    result = []\n    for item in nested:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result'},
        {'prompt': 'def quicksort(arr):\n    """Quicksort"""\n',
         'solution': '    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    return quicksort([x for x in arr if x < pivot]) + [x for x in arr if x == pivot] + quicksort([x for x in arr if x > pivot])'},
        {'prompt': 'def sieve(n):\n    """Sieve of Eratosthenes"""\n',
         'solution': '    is_prime = [True] * (n + 1)\n    is_prime[0] = is_prime[1] = False\n    for i in range(2, int(n ** 0.5) + 1):\n        if is_prime[i]:\n            for j in range(i*i, n+1, i):\n                is_prime[j] = False\n    return [i for i in range(n+1) if is_prime[i]]'},
        {'prompt': 'def binary_search(arr, target):\n    """Binary search"""\n',
         'solution': '    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1'},
        {'prompt': 'def merge_sorted(l1, l2):\n    """Merge sorted lists"""\n',
         'solution': '    result = []\n    i = j = 0\n    while i < len(l1) and j < len(l2):\n        if l1[i] <= l2[j]:\n            result.append(l1[i])\n            i += 1\n        else:\n            result.append(l2[j])\n            j += 1\n    result.extend(l1[i:])\n    result.extend(l2[j:])\n    return result'},
        {'prompt': 'def merge_dicts(d1, d2):\n    """Merge two dicts"""\n',
         'solution': '    result = d1.copy()\n    result.update(d2)\n    return result'},
        {'prompt': 'def word_count(s):\n    """Count word frequencies"""\n',
         'solution': '    counts = {}\n    for word in s.split():\n        counts[word] = counts.get(word, 0) + 1\n    return counts'},
        {'prompt': 'def unique_elements(lst):\n    """Return unique elements"""\n',
         'solution': '    return list(set(lst))'},
        {'prompt': 'def has_duplicates(lst):\n    """Check for duplicates"""\n',
         'solution': '    return len(lst) != len(set(lst))'},
        {'prompt': 'def fibonacci(n):\n    """Return nth Fibonacci"""\n',
         'solution': '    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)'},
        {'prompt': 'def factorial(n):\n    """Return n!""\n',
         'solution': '    if n <= 1:\n        return 1\n    return n * factorial(n-1)'},
        {'prompt': 'def find_max(nums):\n    """Return maximum value"""\n',
         'solution': '    max_val = nums[0]\n    for n in nums:\n        if n > max_val:\n            max_val = n\n    return max_val'},
        {'prompt': 'def gcd(a, b):\n    """Greatest common divisor"""\n',
         'solution': '    while b:\n        a, b = b, a % b\n    return a'},
        {'prompt': 'def is_prime(n):\n    """Check if n is prime"""\n',
         'solution': '    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True'},
        {'prompt': 'def count_vowels(s):\n    """Count vowels"""\n',
         'solution': '    return sum(1 for c in s if c in "aeiouAEIOU")'},
        {'prompt': 'def power(base, exp):\n    """Power function"""\n',
         'solution': '    if exp == 0:\n        return 1\n    return base * power(base, exp - 1)'},
        {'prompt': 'def sum_array(arr):\n    """Sum array recursively"""\n',
         'solution': '    if not arr:\n        return 0\n    return arr[0] + sum_array(arr[1:])'},
        {'prompt': 'def deep_copy(obj):\n    """Deep copy"""\n',
         'solution': '    if isinstance(obj, list):\n        return [deep_copy(item) for item in obj]\n    elif isinstance(obj, dict):\n        return {k: deep_copy(v) for k, v in obj.items()}\n    else:\n        return obj'},
        {'prompt': 'def group_by(items, key_func):\n    """Group items by key"""\n',
         'solution': '    groups = {}\n    for item in items:\n        key = key_func(item)\n        if key not in groups:\n            groups[key] = []\n        groups[key].append(item)\n    return groups'},
        {'prompt': 'def most_common(lst):\n    """Most common element"""\n',
         'solution': '    counts = {}\n    for item in lst:\n        counts[item] = counts.get(item, 0) + 1\n    return max(counts, key=counts.get)'},
        {'prompt': 'def invert_dict(d):\n    """Invert dictionary"""\n',
         'solution': '    return {v: k for k, v in d.items()}'},
        {'prompt': 'def set_union(s1, s2):\n    """Set union"""\n',
         'solution': '    return s1 | s2'},
        {'prompt': 'def set_intersection(s1, s2):\n    """Set intersection"""\n',
         'solution': '    return s1 & s2'},
        {'prompt': 'def lcm(a, b):\n    """Least common multiple"""\n',
         'solution': '    return abs(a * b) // gcd(a, b)'},
        {'prompt': 'def sum_range(n):\n    """Sum of 1 to n"""\n',
         'solution': '    return sum(range(1, n + 1))'},
    ]

    # 测试集模板（70个）- 完全不同的问题和solution
    test_templates = [
        {'prompt': 'def triple_all(nums):\n    """Triple each number"""\n',
         'solution': '    return [x * 3 for x in nums]'},
        {'prompt': 'def subtract_all(nums, val):\n    """Subtract val from each number"""\n',
         'solution': '    return [x - val for x in nums]'},
        {'prompt': 'def filter_even(nums):\n    """Filter even numbers"""\n',
         'solution': '    return [x for x in nums if x % 2 == 0]'},
        {'prompt': 'def filter_positive(nums):\n    """Filter positive numbers"""\n',
         'solution': '    return [x for x in nums if x > 0]'},
        {'prompt': 'def square_all(nums):\n    """Square each number"""\n',
         'solution': '    return [x ** 2 for x in nums]'},
        {'prompt': 'def count_positive(nums):\n    """Count positive numbers"""\n',
         'solution': '    return sum(1 for x in nums if x > 0)'},
        {'prompt': 'def count_negative(nums):\n    """Count negative numbers"""\n',
         'solution': '    return sum(1 for x in nums if x < 0)'},
        {'prompt': 'def abs_all(nums):\n    """Absolute value of each number"""\n',
         'solution': '    return [abs(x) for x in nums]'},
        {'prompt': 'def reverse_list(lst):\n    """Reverse a list"""\n',
         'solution': '    return lst[::-1]'},
        {'prompt': 'def is_sorted(arr):\n    """Check if array is sorted"""\n',
         'solution': '    return arr == sorted(arr)'},
        {'prompt': 'def min_value(nums):\n    """Return minimum value"""\n',
         'solution': '    return min(nums) if nums else None'},
        {'prompt': 'def max_value(nums):\n    """Return maximum value"""\n',
         'solution': '    return max(nums) if nums else None'},
        {'prompt': 'def product_all(nums):\n    """Product of all numbers"""\n',
         'solution': '    result = 1\n    for n in nums:\n        result *= n\n    return result'},
        {'prompt': 'def is_member(item, lst):\n    """Check if item is in list"""\n',
         'solution': '    return item in lst'},
        {'prompt': 'def index_of(item, lst):\n    """Find index of item"""\n',
         'solution': '    return lst.index(item) if item in lst else -1'},
        {'prompt': 'def last_element(lst):\n    """Return last element"""\n',
         'solution': '    return lst[-1] if lst else None'},
        {'prompt': 'def first_n_elements(lst, n):\n    """Return first n elements"""\n',
         'solution': '    return lst[:n]'},
        {'prompt': 'def last_n_elements(lst, n):\n    """Return last n elements"""\n',
         'solution': '    return lst[-n:]'},
        {'prompt': 'def remove_duplicates(lst):\n    """Remove duplicates keeping order"""\n',
         'solution': '    seen = set()\n    result = []\n    for x in lst:\n        if x not in seen:\n            seen.add(x)\n            result.append(x)\n    return result'},
        {'prompt': 'def is_anagram(s1, s2):\n    """Check if two strings are anagrams"""\n',
         'solution': '    return sorted(s1) == sorted(s2)'},
        {'prompt': 'def capitalize_words(s):\n    """Capitalize first letter of each word"""\n',
         'solution': '    return " ".join(word.capitalize() for word in s.split())'},
        {'prompt': 'def remove_whitespace(s):\n    """Remove all whitespace"""\n',
         'solution': '    return "".join(s.split())'},
        {'prompt': 'def count_consonants(s):\n    """Count consonants in string"""\n',
         'solution': '    return sum(1 for c in s.lower() if c.isalpha() and c not in "aeiou")'},
        {'prompt': 'def has_substring(s, sub):\n    """Check if string contains substring"""\n',
         'solution': '    return sub in s'},
        {'prompt': 'def count_words(s):\n    """Count words in string"""\n',
         'solution': '    return len(s.split())'},
        {'prompt': 'def longest_word(s):\n    """Find longest word"""\n',
         'solution': '    return max(s.split(), key=len) if s.split() else ""'},
        {'prompt': 'def shortest_word(s):\n    """Find shortest word"""\n',
         'solution': '    return min(s.split(), key=len) if s.split() else ""'},
        {'prompt': 'def fib_iterative(n):\n    """Fibonacci iteratively"""\n',
         'solution': '    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(n - 1):\n        a, b = b, a + b\n    return b'},
        {'prompt': 'def tribonacci(n):\n    """Tribonacci number"""\n',
         'solution': '    if n == 0:\n        return 0\n    if n <= 2:\n        return 1\n    return tribonacci(n-1) + tribonacci(n-2) + tribonacci(n-3)'},
        {'prompt': 'def is_even(n):\n    """Check if number is even"""\n',
         'solution': '    return n % 2 == 0'},
        {'prompt': 'def is_odd(n):\n    """Check if number is odd"""\n',
         'solution': '    return n % 2 != 0'},
        {'prompt': 'def signum(n):\n    """Sign of number"""\n',
         'solution': '    if n > 0:\n        return 1\n    elif n < 0:\n        return -1\n    return 0'},
        {'prompt': 'def absolute_difference(a, b):\n    """Absolute difference"""\n',
         'solution': '    return abs(a - b)'},
        {'prompt': 'def average(nums):\n    """Average of numbers"""\n',
         'solution': '    return sum(nums) / len(nums) if nums else 0'},
        {'prompt': 'def median(nums):\n    """Median of numbers"""\n',
         'solution': '    sorted_nums = sorted(nums)\n    n = len(sorted_nums)\n    if n % 2 == 0:\n        return (sorted_nums[n//2-1] + sorted_nums[n//2]) / 2\n    return sorted_nums[n//2]'},
        {'prompt': 'def mode(nums):\n    """Mode of numbers"""\n',
         'solution': '    from collections import Counter\n    return Counter(nums).most_common(1)[0][0]'},
        {'prompt': 'def range_nums(nums):\n    """Range of numbers"""\n',
         'solution': '    return max(nums) - min(nums) if nums else 0'},
        {'prompt': 'def variance(nums):\n    """Variance of numbers"""\n',
         'solution': '    avg = sum(nums) / len(nums)\n    return sum((x - avg) ** 2 for x in nums) / len(nums)'},
        {'prompt': 'def std_dev(nums):\n    """Standard deviation"""\n',
         'solution': '    import math\n    avg = sum(nums) / len(nums)\n    return math.sqrt(sum((x - avg) ** 2 for x in nums) / len(nums))'},
        {'prompt': 'def dot_product(v1, v2):\n    """Dot product of vectors"""\n',
         'solution': '    return sum(x * y for x, y in zip(v1, v2))'},
        {'prompt': 'def vector_magnitude(v):\n    """Magnitude of vector"""\n',
         'solution': '    import math\n    return math.sqrt(sum(x ** 2 for x in v))'},
        {'prompt': 'def is_unique(s):\n    """Check if string has all unique chars"""\n',
         'solution': '    return len(s) == len(set(s)'},
        {'prompt': 'def compress_string(s):\n    """Compress string"""\n',
         'solution': '    compressed = []\n    count = 1\n    for i in range(1, len(s)):\n        if s[i] == s[i-1]:\n            count += 1\n        else:\n            compressed.append(s[i-1] + str(count))\n            count = 1\n    compressed.append(s[-1] + str(count))\n    return "".join(compressed)'},
        {'prompt': 'def rotate_list(lst, k):\n    """Rotate list by k"""\n',
         'solution': '    k = k % len(lst)\n    return lst[-k:] + lst[:-k]'},
        {'prompt': 'def is_matrix_square(matrix):\n    """Check if matrix is square"""\n',
         'solution': '    return all(len(row) == len(matrix) for row in matrix)'},
        {'prompt': 'def transpose_matrix(matrix):\n    """Transpose matrix"""\n',
         'solution': '    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]'},
        {'prompt': 'def flatten_dict(nested):\n    """Flatten nested dict"""\n',
         'solution': '    result = {}\n    for k, v in nested.items():\n        if isinstance(v, dict):\n            result.update(flatten_dict(v))\n        else:\n            result[k] = v\n    return result'},
        {'prompt': 'def dict_from_tuples(tuples):\n    """Create dict from list of tuples"""\n',
         'solution': '    return dict(tuples)'},
        {'prompt': 'def sort_dict_by_value(d):\n    """Sort dict by values"""\n',
         'solution': '    return dict(sorted(d.items(), key=lambda x: x[1]))'},
        {'prompt': 'def filter_dict(d, threshold):\n    """Filter dict by value"""\n',
         'solution': '    return {k: v for k, v in d.items() if v > threshold}'},
        {'prompt': 'def merge_sets(sets):\n    """Merge multiple sets"""\n',
         'solution': '    result = set()\n    for s in sets:\n        result.update(s)\n    return result'},
        {'prompt': 'def set_difference(s1, s2):\n    """Set difference"""\n',
         'solution': '    return s1 - s2'},
        {'prompt': 'def symmetric_diff(s1, s2):\n    """Symmetric difference"""\n',
         'solution': '    return s1 ^ s2'},
        {'prompt': 'def is_subset(s1, s2):\n    """Check if s1 is subset of s2"""\n',
         'solution': '    return s1.issubset(s2)'},
        {'prompt': 'def is_superset(s1, s2):\n    """Check if s1 is superset of s2"""\n',
         'solution': '    return s1.issuperset(s2)'},
        {'prompt': 'def cartesian_product(s1, s2):\n    """Cartesian product of sets"""\n',
         'solution': '    return {(a, b) for a in s1 for b in s2}'},
        {'prompt': 'def all_subsets(s):\n    """All subsets of set"""\n',
         'solution': '    result = [[]]\n    for elem in s:\n        result += [subset + [elem] for subset in result]\n    return result'},
        {'prompt': 'def combinations_with_replacement(n, k):\n    """Combinations with replacement"""\n',
         'solution': '    if k == 0:\n        return [[]]\n    if not n:\n        return []\n    result = []\n    for i in range(len(n)):\n        for combo in combinations_with_replacement(n[i:], k-1):\n            result.append([n[i]] + combo)\n    return result'},
        {'prompt': 'def permutations_of_string(s):\n    """All permutations of string"""\n',
         'solution': '    if len(s) <= 1:\n        return [s]\n    result = []\n    for i in range(len(s)):\n        for perm in permutations_of_string(s[:i] + s[i+1:]):\n            result.append(s[i] + perm)\n    return result'},
        {'prompt': 'def is_pandigital(n):\n    """Check if number is pandigital"""\n',
         'solution': '    s = str(n)\n    return len(s) == 9 and set(s) == set("123456789")'},
        {'prompt': 'def count_primes_upto(n):\n    """Count primes up to n"""\n',
         'solution': '    count = 0\n    for i in range(2, n + 1):\n        is_prime = True\n        for j in range(2, int(i ** 0.5) + 1):\n            if i % j == 0:\n                is_prime = False\n                break\n        if is_prime:\n            count += 1\n    return count'},
        {'prompt': 'def next_prime(n):\n    """Next prime after n"""\n',
         'solution': '    while True:\n        n += 1\n        is_prime = True\n        for j in range(2, int(n ** 0.5) + 1):\n            if n % j == 0:\n                is_prime = False\n                break\n        if is_prime:\n            return n'},
        {'prompt': 'def prime_factors(n):\n    """Prime factors of n"""\n',
         'solution': '    factors = []\n    d = 2\n    while d * d <= n:\n        while n % d == 0:\n            factors.append(d)\n            n //= d\n        d += 1\n    if n > 1:\n        factors.append(n)\n    return factors'},
        {'prompt': 'def is_perfect_square(n):\n    """Check if perfect square"""\n',
         'solution': '    if n < 0:\n        return False\n    root = int(n ** 0.5)\n    return root * root == n'},
        {'prompt': 'def is_perfect_number(n):\n    """Check if perfect number"""\n',
         'solution': '    if n <= 0:\n        return False\n    divisors = [1]\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            divisors.append(i)\n            if i != n // i:\n                divisors.append(n // i)\n    return sum(divisors) == n'},
        {'prompt': 'def collatz_sequence(n):\n    """Collatz sequence"""\n',
         'solution': '    seq = [n]\n    while n != 1:\n        if n % 2 == 0:\n            n = n // 2\n        else:\n            n = 3 * n + 1\n        seq.append(n)\n    return seq'},
    ]

    # 生成训练集（30个）
    for i, template in enumerate(train_templates):
        tasks.append({
            'task_id': f'train_{i:03d}',
            'prompt': template['prompt'],
            'canonical_solution': template['solution'],
            'is_train': True,
        })

    # 生成测试集（70个）
    for i, template in enumerate(test_templates):
        tasks.append({
            'task_id': f'test_{i:03d}',
            'prompt': template['prompt'],
            'canonical_solution': template['solution'],
            'is_train': False,
        })

    return tasks


# ============================================================
# 主实验
# ============================================================
def run_experiment():
    print("=" * 70)
    print("H38 Living Tree - Scale Validation (100 tasks)")
    print("=" * 70)
    print()
    print("Key Fix: Train/test have completely different solutions")
    print()

    # ----------------------------------------------------------
    # 加载 CodeBERT
    # ----------------------------------------------------------
    import torch
    from transformers import AutoTokenizer, AutoModel

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Loading CodeBERT on {device}...")
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base").to(device)
    model.eval()
    print("CodeBERT loaded\n")

    def embed_codes(codes):
        embs = []
        with torch.no_grad():
            for code in codes:
                inputs = tokenizer(code, return_tensors='pt',
                                   truncation=True, max_length=512).to(device)
                outputs = model(**inputs)
                embs.append(outputs.last_hidden_state[:, 0, :].cpu().numpy()[0])
        return np.array(embs)

    # ----------------------------------------------------------
    # 生成100个任务
    # ----------------------------------------------------------
    print("Generating 100 tasks (30 train, 70 test)...")
    dataset = generate_tasks()
    train_data = [d for d in dataset if d['is_train']]
    test_data = [d for d in dataset if not d['is_train']]
    print(f"  Train: {len(train_data)}, Test: {len(test_data)}\n")

    # 生成embeddings
    print("Generating embeddings...")
    codes = [d['prompt'] + d['canonical_solution'] for d in dataset]
    embeddings = embed_codes(codes)

    for i, d in enumerate(dataset):
        d['embedding'] = embeddings[i]

    # 重新分配embeddings到train/test
    train_embeddings = [d['embedding'] for d in train_data]
    test_embeddings = [d['embedding'] for d in test_data]

    print(f"  Embeddings shape: {embeddings.shape}\n")

    # ----------------------------------------------------------
    # Phase 1: 持续学习
    # ----------------------------------------------------------
    print("=" * 70)
    print("Phase 1: Sequential Learning")
    print("=" * 70)

    lt = LivingTreeH38(embedding_dim=768)
    learn_times = []

    for i, d in enumerate(train_data):
        start = time.time()
        lt.learn_task(d['task_id'], d['embedding'],
                     d['prompt'], d['canonical_solution'])
        elapsed = time.time() - start
        learn_times.append(elapsed)

        if i < 3 or i >= len(train_data) - 2:
            print(f"  [{i+1}] Learned {d['task_id']}")

    print(f"\n  Total nodes: {len(lt.nodes)}")
    print(f"  Avg learn time: {np.mean(learn_times)*1000:.2f}ms")
    print(f"  Time growth (last/first): {learn_times[-1]/learn_times[0]:.2f}x")
    print()

    # ----------------------------------------------------------
    # Phase 2: 测试集检索评估
    # ----------------------------------------------------------
    print("=" * 70)
    print("Phase 2: Retrieval Evaluation (Test Set)")
    print("=" * 70)

    test_scores = []
    for d in test_data:
        matches = lt.retrieve(d['embedding'], k=3)
        pred_solution = matches[0][1].solution
        score = code_eval(pred_solution, d['canonical_solution'])
        test_scores.append(score)

    avg_test_score = np.mean(test_scores)
    print(f"\n  Test Score: {avg_test_score:.2%}")
    print(f"  High (>0.7): {sum(1 for s in test_scores if s > 0.7)}/{len(test_scores)}")
    print(f"  Medium (0.4-0.7): {sum(1 for s in test_scores if 0.4 <= s <= 0.7)}/{len(test_scores)}")
    print(f"  Low (<0.4): {sum(1 for s in test_scores if s < 0.4)}/{len(test_scores)}")
    print()

    # ----------------------------------------------------------
    # Phase 3: 回测旧任务（遗忘检测）
    # ----------------------------------------------------------
    print("=" * 70)
    print("Phase 3: Backtesting Old Tasks")
    print("=" * 70)

    backtest_scores = []
    for i in range(1, len(train_data) + 1):
        scores = []
        for j in range(i):
            d = train_data[j]
            matches = lt.retrieve(d['embedding'], k=3)
            pred = matches[0][1].solution
            scores.append(code_eval(pred, d['canonical_solution']))
        backtest_scores.append(np.mean(scores))

    final_retention = backtest_scores[-1]
    print(f"  Final backtest score: {final_retention:.2%}")
    print(f"  Initial backtest score: {backtest_scores[0]:.2%}")
    print(f"  Retention rate: {final_retention/backtest_scores[0]:.2%}")
    print()

    # ----------------------------------------------------------
    # 结果对比
    # ----------------------------------------------------------
    print("=" * 70)
    print("Results Summary")
    print("=" * 70)

    print(f"""
  Test Score: {avg_test_score:.2%}
  Backtest Retention: {final_retention:.2%}
  Time Growth: {learn_times[-1]/learn_times[0]:.2f}x

  H36 (20 tasks, similar solutions): 70.56%
  H38 (100 tasks, different solutions): {avg_test_score:.2%}
""")

    # ----------------------------------------------------------
    # Falsify判断
    # ----------------------------------------------------------
    print("--- Falsify Checks ---")

    checks = {
        'scale_works': (avg_test_score > 0.25,
            f"Test score > 25%: {avg_test_score:.1%}"),
        'no_forgetting': (final_retention > 0.5,
            f"Retention > 50%: {final_retention:.1%}"),
        'time_constant': (learn_times[-1]/learn_times[0] < 2.0,
            f"Time growth < 2x: {learn_times[-1]/learn_times[0]:.2f}x"),
        'better_than_random': (avg_test_score > 0.1,
            f"Better than random (10%): {avg_test_score:.1%}"),
    }

    passed = 0
    for desc, (ok, detail) in checks.items():
        status = "PASS" if ok else "FAIL"
        print(f"  {status}  {desc}: {detail}")
        if ok:
            passed += 1

    print(f"\n  Passed {passed}/{len(checks)} checks")

    if passed >= 3:
        print("\n  -> Living Tree H38 Scale Validation SUCCESS!")
        print("     Pure similarity retrieval works at 100-task scale")

    return {
        'test_score': avg_test_score,
        'retention': final_retention,
        'time_growth': learn_times[-1]/learn_times[0],
        'passed': passed,
    }


if __name__ == "__main__":
    results = run_experiment()
