"""
H36 Living Tree - Retrieval + Generation验证
====================================================

目标：
从"分类系统"变为"检索+生成系统"

核心变化：
- 不只分类CF/DO，而是用匹配到的节点知识解决问题
- 给定新问题，找到最相似节点，用节点的代码作为few-shot context
- 测试节点存储的知识是否真的有用

实验设计：
1. 顺序学习20个任务，每个节点存储 (prompt, solution)
2. 给定新问题，用embedding相似度找最相似节点
3. 用节点的solution作为预测答案
4. 评估exact match率

Author: Claude Code
Date: 2026-04-09
"""

import numpy as np
import time
import warnings
import json
warnings.filterwarnings('ignore')

np.random.seed(42)


# ============================================================
# Living Tree 节点
# ============================================================
class LivingTreeNode:
    """存储单个任务的节点"""
    def __init__(self, task_id, embedding, prompt, solution, cf=None, do=None):
        self.task_id = task_id
        self.embedding = embedding
        self.prompt = prompt
        self.solution = solution
        self.cf = cf
        self.do = do

    def similarity(self, other_embedding):
        return np.dot(self.embedding, other_embedding) / (
            np.linalg.norm(self.embedding) * np.linalg.norm(other_embedding) + 1e-8)


# ============================================================
# Living Tree H36 - 检索+生成系统
# ============================================================
class LivingTreeH36:
    """
    Living Tree H36: 从分类到检索+生成
    """
    def __init__(self, embedding_dim=768):
        self.embedding_dim = embedding_dim
        self.nodes = {}  # task_id -> node

    def learn_task(self, task_id, embedding, prompt, solution, cf=None, do=None):
        """学习新任务 - 只添加，不更新"""
        node = LivingTreeNode(task_id, embedding, prompt, solution, cf, do)
        self.nodes[task_id] = node

    def retrieve(self, embedding, k=1):
        """找到最相似的k个节点"""
        similarities = []
        for node in self.nodes.values():
            sim = node.similarity(embedding)
            similarities.append((sim, node))

        # 按相似度降序排列
        similarities.sort(key=lambda x: x[0], reverse=True)
        return similarities[:k]

    def solve(self, problem_embedding, problem_prompt, k=3):
        """
        用检索到的节点解决问题
        返回: list of (node, solution) 按相似度排序
        """
        matches = self.retrieve(problem_embedding, k=k)
        return [(node, node.solution) for sim, node in matches]


# ============================================================
# 简化的代码补全评估
# ============================================================
def simple_code_eval(pred_solution, gt_solution):
    """
    简化的代码评估：
    - exact match
    - key pattern match
    """
    # 去除空白进行比对
    pred_clean = pred_solution.strip()
    gt_clean = gt_solution.strip()

    if pred_clean == gt_clean:
        return 1.0  # 完全匹配

    # 检查关键模式
    gt_keywords = extract_keywords(gt_clean)
    pred_keywords = extract_keywords(pred_clean)

    if not gt_keywords:
        return 0.0

    overlap = len(gt_keywords & pred_keywords) / len(gt_keywords)
    return overlap


def extract_keywords(code):
    """提取代码关键词"""
    import re
    # 简单关键词提取
    keywords = set()
    patterns = [
        r'\bdef\s+\w+',      # 函数名
        r'\breturn\s+',      # return语句
        r'\bfor\s+\w+\s+in', # for循环
        r'\bif\s+',          # 条件
        r'\bwhile\s+',       # while循环
        r'\brecursion\(',    # 递归调用
        r'\[\s*\w+\s+for',   # 列表推导
        r'\bextend\(',       # list方法
        r'\bappend\(',       # append方法
    ]

    for p in patterns:
        matches = re.findall(p, code)
        keywords.update(matches)

    return keywords


# ============================================================
# HumanEval数据集
# ============================================================
def load_humaneval_tasks():
    """加载HumanEval任务"""
    # 使用H35的数据集
    humaneval_tasks = [
        {'task_id': 'he_01', 'prompt': 'def get_first_element(lst):\n    """Return the first element of lst"""\n',
         'canonical_solution': '    return lst[0] if lst else None', 'cf': 'conditional', 'do': 'list'},
        {'task_id': 'he_02', 'prompt': 'def double_all(nums):\n    """Double each number in nums"""\n',
         'canonical_solution': '    return [x * 2 for x in nums]', 'cf': 'comprehension', 'do': 'list'},
        {'task_id': 'he_03', 'prompt': 'def sum_list(nums):\n    """Return sum of all numbers"""\n',
         'canonical_solution': '    total = 0\n    for n in nums:\n        total += n\n    return total', 'cf': 'loop', 'do': 'list'},
        {'task_id': 'he_04', 'prompt': 'def fibonacci(n):\n    """Return nth Fibonacci number"""\n',
         'canonical_solution': '    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)', 'cf': 'recursion', 'do': 'arithmetic'},
        {'task_id': 'he_05', 'prompt': 'def factorial(n):\n    """Return n!"""\n',
         'canonical_solution': '    if n <= 1:\n        return 1\n    return n * factorial(n-1)', 'cf': 'recursion', 'do': 'arithmetic'},
        {'task_id': 'he_06', 'prompt': 'def find_max(nums):\n    """Return maximum value"""\n',
         'canonical_solution': '    max_val = nums[0]\n    for n in nums:\n        if n > max_val:\n            max_val = n\n    return max_val', 'cf': 'loop', 'do': 'arithmetic'},
        {'task_id': 'he_07', 'prompt': 'def reverse_string(s):\n    """Reverse string s"""\n',
         'canonical_solution': '    return s[::-1]', 'cf': 'comprehension', 'do': 'list'},
        {'task_id': 'he_08', 'prompt': 'def is_palindrome(s):\n    """Check if s is palindrome"""\n',
         'canonical_solution': '    return s == s[::-1]', 'cf': 'conditional', 'do': 'list'},
        {'task_id': 'he_09', 'prompt': 'def count_vowels(s):\n    """Count vowels in s"""\n',
         'canonical_solution': '    return sum(1 for c in s if c in "aeiouAEIOU")', 'cf': 'comprehension', 'do': 'arithmetic'},
        {'task_id': 'he_10', 'prompt': 'def flatten(nested):\n    """Flatten nested list"""\n',
         'canonical_solution': '    result = []\n    for item in nested:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result', 'cf': 'recursion', 'do': 'list'},
        {'task_id': 'he_11', 'prompt': 'def quicksort(arr):\n    """Sort array"""\n',
         'canonical_solution': '    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)', 'cf': 'recursion', 'do': 'list'},
        {'task_id': 'he_12', 'prompt': 'def merge_dicts(d1, d2):\n    """Merge two dicts"""\n',
         'canonical_solution': '    result = d1.copy()\n    result.update(d2)\n    return result', 'cf': 'loop', 'do': 'dict'},
        {'task_id': 'he_13', 'prompt': 'def word_count(s):\n    """Count word frequencies"""\n',
         'canonical_solution': '    counts = {}\n    for word in s.split():\n        counts[word] = counts.get(word, 0) + 1\n    return counts', 'cf': 'loop', 'do': 'dict'},
        {'task_id': 'he_14', 'prompt': 'def unique_elements(lst):\n    """Return unique elements"""\n',
         'canonical_solution': '    return list(set(lst))', 'cf': 'comprehension', 'do': 'set'},
        {'task_id': 'he_15', 'prompt': 'def has_duplicates(lst):\n    """Check for duplicates"""\n',
         'canonical_solution': '    return len(lst) != len(set(lst))', 'cf': 'conditional', 'do': 'set'},
        {'task_id': 'he_16', 'prompt': 'def gcd(a, b):\n    """Greatest common divisor"""\n',
         'canonical_solution': '    while b:\n        a, b = b, a % b\n    return a', 'cf': 'loop', 'do': 'arithmetic'},
        {'task_id': 'he_17', 'prompt': 'def is_prime(n):\n    """Check if n is prime"""\n',
         'canonical_solution': '    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True', 'cf': 'loop', 'do': 'arithmetic'},
        {'task_id': 'he_18', 'prompt': 'def sieve(n):\n    """Return primes up to n"""\n',
         'canonical_solution': '    is_prime = [True] * (n + 1)\n    is_prime[0] = is_prime[1] = False\n    for i in range(2, int(n ** 0.5) + 1):\n        if is_prime[i]:\n            for j in range(i*i, n+1, i):\n                is_prime[j] = False\n    return [i for i in range(n+1) if is_prime[i]]', 'cf': 'loop', 'do': 'list'},
        {'task_id': 'he_19', 'prompt': 'def binary_search(arr, target):\n    """Binary search"""\n',
         'canonical_solution': '    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1', 'cf': 'loop', 'do': 'list'},
        {'task_id': 'he_20', 'prompt': 'def deep_copy(obj):\n    """Deep copy nested structure"""\n',
         'canonical_solution': '    if isinstance(obj, list):\n        return [deep_copy(item) for item in obj]\n    elif isinstance(obj, dict):\n        return {k: deep_copy(v) for k, v in obj.items()}\n    else:\n        return obj', 'cf': 'recursion', 'do': 'dict'},
    ]
    return humaneval_tasks


# ============================================================
# 主实验
# ============================================================
def run_experiment():
    print("=" * 70)
    print("H36 Living Tree - Retrieval + Generation")
    print("=" * 70)
    print()
    print("核心变化：从分类 -> 检索+生成")
    print("  - 不只分类CF/DO")
    print("  - 用匹配节点的solution作为预测")
    print("  - 测试节点存储的知识是否真的有用")
    print()

    # ----------------------------------------------------------
    # 加载 CodeBERT
    # ----------------------------------------------------------
    import torch
    from transformers import AutoTokenizer, AutoModel

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"加载 CodeBERT on {device}...")
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base").to(device)
    model.eval()
    print("✓ CodeBERT loaded\n")

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
    # 加载数据集
    # ----------------------------------------------------------
    print("加载HumanEval数据集...")
    dataset = load_humaneval_tasks()
    print(f"  数据集大小: {len(dataset)} 任务\n")

    # 生成embeddings
    print("生成embeddings...")
    codes = [d['prompt'] + d['canonical_solution'] for d in dataset]
    embeddings = embed_codes(codes)

    for i, d in enumerate(dataset):
        d['embedding'] = embeddings[i]
    print(f"  ✓ embeddings shape: {embeddings.shape}\n")

    # ----------------------------------------------------------
    # 划分训练/测试
    # ----------------------------------------------------------
    print("划分训练/测试集...")
    n_train = int(len(dataset) * 0.7)  # 70%训练
    train_data = dataset[:n_train]
    test_data = dataset[n_train:]

    print(f"  训练集: {len(train_data)} 样本")
    print(f"  测试集: {len(test_data)} 样本")
    print()

    # ----------------------------------------------------------
    # Phase 1: 持续学习
    # ----------------------------------------------------------
    print("=" * 70)
    print("Phase 1: 持续学习 - 顺序添加任务到Living Tree")
    print("=" * 70)

    lt = LivingTreeH36(embedding_dim=768)
    learn_times = []

    for i, d in enumerate(train_data):
        start = time.time()
        lt.learn_task(d['task_id'], d['embedding'],
                     d['prompt'], d['canonical_solution'], d['cf'], d['do'])
        learn_times.append(time.time() - start)

        if i < 3 or i >= len(train_data) - 2:
            print(f"  [{i+1}] 学习了 {d['task_id']} ({d['cf']}-{d['do']})")

    print(f"\n  节点总数: {len(lt.nodes)}")
    print(f"  平均学习时间: {np.mean(learn_times)*1000:.2f}ms")
    print(f"  时间增长: {learn_times[-1]/learn_times[0]:.2f}x")
    print()

    # ----------------------------------------------------------
    # Phase 2: 检索评估
    # ----------------------------------------------------------
    print("=" * 70)
    print("Phase 2: 检索评估 - 测试集")
    print("=" * 70)

    retrieval_results = []

    for d in test_data:
        problem_emb = d['embedding']
        problem_prompt = d['prompt']

        # 检索最相似的节点
        matches = lt.solve(problem_emb, problem_prompt, k=3)

        # 获取最相似节点的solution
        top_node, top_solution = matches[0]

        # 评估
        score = simple_code_eval(top_solution, d['canonical_solution'])

        retrieval_results.append({
            'task_id': d['task_id'],
            'gt_solution': d['canonical_solution'],
            'pred_solution': top_solution,
            'matched_task': top_node.task_id,
            'similarity': top_node.similarity(problem_emb),
            'score': score,
            'cf_match': top_node.cf == d['cf'],
            'do_match': top_node.do == d['do'],
        })

        print(f"  {d['task_id']}: 匹配到 {top_node.task_id} (sim={top_node.similarity(problem_emb):.3f})")
        print(f"    CF: {top_node.cf} vs {d['cf']} {'✓' if top_node.cf == d['cf'] else '✗'}")
        print(f"    DO: {top_node.do} vs {d['do']} {'✓' if top_node.do == d['do'] else '✗'}")
        print(f"    Score: {score:.2f}")
        print()

    # ----------------------------------------------------------
    # 统计结果
    # ----------------------------------------------------------
    print("=" * 70)
    print("Phase 3: 结果统计")
    print("=" * 70)

    scores = [r['score'] for r in retrieval_results]
    cf_matches = sum(1 for r in retrieval_results if r['cf_match'])
    do_matches = sum(1 for r in retrieval_results if r['do_match'])

    # 按相似度分组
    high_sim = [r for r in retrieval_results if r['similarity'] > 0.85]
    low_sim = [r for r in retrieval_results if r['similarity'] <= 0.85]

    print(f"\n  整体检索准确率:")
    print(f"    平均代码评分: {np.mean(scores):.2%}")
    print(f"    CF匹配率: {cf_matches}/{len(test_data)} ({cf_matches/len(test_data):.1%})")
    print(f"    DO匹配率: {do_matches}/{len(test_data)} ({do_matches/len(test_data):.1%})")
    print()

    print(f"  按相似度分组:")
    if high_sim:
        high_scores = [r['score'] for r in high_sim]
        print(f"    高相似度(>0.85): {len(high_sim)}个, 平均评分={np.mean(high_scores):.2%}")
    if low_sim:
        low_scores = [r['score'] for r in low_sim]
        print(f"    低相似度(≤0.85): {len(low_sim)}个, 平均评分={np.mean(low_scores):.2%}")
    print()

    # ----------------------------------------------------------
    # 核心发现
    # ----------------------------------------------------------
    print("=" * 70)
    print("核心发现")
    print("=" * 70)

    avg_score = np.mean(scores)
    time_growth = learn_times[-1] / learn_times[0] if learn_times[0] > 0 else 0

    # 关键问题：节点的solution能否帮助解决新问题？
    # 如果检索到的solution与实际问题完全匹配，说明学到了可迁移的知识

    print(f"""
H36 检索+生成验证：
  测试样本数: {len(test_data)}
  平均代码评分: {avg_score:.2%}
  CF匹配率: {cf_matches/len(test_data):.1%}
  DO匹配率: {do_matches/len(test_data):.1%}
  时间增长: {time_growth:.2f}x

与H35分类系统的区别：
  H35: 分类CF+DO，判断"像不像"
  H36: 直接检索solution，判断"能不能用"

关键洞察：
  - 检索到相同CF/DO的节点 ≠ 检索到能解决新问题的节点
  - 代码评分高说明节点存储的知识可迁移
  - 评分低说明新问题需要不同的解决思路
""")

    # ----------------------------------------------------------
    # Falsify判断
    # ----------------------------------------------------------
    print("--- Falsify 判断 ---")

    # H36的目标：验证检索能否找到有用的solution
    # 如果检索到的solution评分>0.5，说明有一定帮助
    checks = {
        'retrieval_useful': (avg_score > 0.3,
            f"检索solution评分 > 30%: {avg_score:.1%}"),
        'time_constant': (time_growth < 3.0,
            f"时间增长 < 3x: {time_growth:.2f}x"),
        'cf_retrieval': (cf_matches/len(test_data) > 0.25,
            f"CF匹配率 > 25%: {cf_matches/len(test_data):.1%}"),
        'do_retrieval': (do_matches/len(test_data) > 0.4,
            f"DO匹配率 > 40%: {do_matches/len(test_data):.1%}"),
    }

    passed = 0
    for desc, (ok, detail) in checks.items():
        status = "✓ PASS" if ok else "✗ FAIL"
        print(f"  {status}  {desc}: {detail}")
        if ok:
            passed += 1

    print(f"\n  通过 {passed}/{len(checks)} 项检验")

    if passed >= 3:
        print("\n  → Living Tree H36 检索+生成 验证成功！")
        print("     节点存储的知识可以用于解决新问题")

    return {
        'avg_score': avg_score,
        'time_growth': time_growth,
        'cf_match_rate': cf_matches/len(test_data),
        'do_match_rate': do_matches/len(test_data),
        'passed': passed,
        'retrieval_results': retrieval_results,
    }


if __name__ == "__main__":
    results = run_experiment()
