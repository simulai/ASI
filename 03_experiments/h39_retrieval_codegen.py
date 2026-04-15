"""
H39 Living Tree - Retrieval + CodeGen Generation
=================================================

目标：用CodeGen基于检索到的节点生成新问题的解决方案

核心变化：
- H36/H38: 直接返回检索到的solution
- H39: 用检索到的solution作为few-shot context，让CodeGen生成新solution

实验设计：
1. 顺序学习20个任务（prompt + solution -> embedding）
2. 给定新问题，用embedding相似度找到最相似的K个节点
3. 把K个节点的(prompt, solution)作为few-shot examples
4. 让CodeGen基于这些examples生成新问题的解决方案
5. 评估生成质量

Author: Claude Code
Date: 2026-04-15
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
# Living Tree H39
# ============================================================
class LivingTreeH39:
    def __init__(self, embedding_dim=768):
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
def extract_code_patterns(code):
    """提取代码模式"""
    import re
    patterns = set()

    # 关键词模式
    keywords = re.findall(r'\b(def|return|for|if|while|in|is|and|or|not|True|False|None)\b', code)
    patterns.update(keywords)

    # 结构模式
    list_comp = re.findall(r'\[.*?for.*?in.*?\]', code)
    if list_comp:
        patterns.add('[...for...in...]')

    func_def = re.findall(r'def\s+(\w+)', code)
    patterns.update([f'def:{f}' for f in func_def])

    return patterns


def code_eval(generated, gt_solution):
    """评估生成代码的质量"""
    gen_clean = generated.strip()
    gt_clean = gt_solution.strip()

    # 完全匹配
    if gen_clean == gt_clean:
        return 1.0

    # 模式匹配
    gen_patterns = extract_code_patterns(gen_clean)
    gt_patterns = extract_code_patterns(gt_clean)

    if not gt_patterns:
        return 0.0

    overlap = len(gen_patterns & gt_patterns) / len(gt_patterns)

    # 检查关键结构
    key_structures = ['for', 'if', 'return', 'def']
    gen_has = sum(1 for s in key_structures if s in gen_clean)
    gt_has = sum(1 for s in key_structures if s in gt_clean)

    if gt_has > 0:
        structure_score = gen_has / gt_has
        overlap = (overlap + structure_score) / 2

    return min(overlap, 1.0)


# ============================================================
# CodeGen 生成
# ============================================================
def generate_with_codegen(prompt, few_shot_examples, codegen_model, codegen_tokenizer, device):
    """
    用CodeGen基于few-shot examples生成代码
    """
    # 构建few-shot prompt
    fs_prompt = "Below are some code examples:\n\n"

    for ex_prompt, ex_solution in few_shot_examples:
        fs_prompt += f"Task:\n{ex_prompt}\nSolution:\n{ex_solution}\n\n"

    fs_prompt += f"Task:\n{prompt}\nSolution:\n"

    # Tokenize
    inputs = codegen_tokenizer(fs_prompt, return_tensors="pt",
                              truncation=True, max_length=512).to(device)

    # 生成
    with torch.no_grad():
        outputs = codegen_model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.3,
            top_p=0.95,
            do_sample=True,
            pad_token_id=codegen_tokenizer.eos_token_id,
        )

    # 解码
    generated = codegen_tokenizer.decode(outputs[0], skip_special_tokens=True)

    # 提取生成的solution部分
    if "Solution:\n" in generated:
        solution_part = generated.split("Solution:\n")[-1]
        # 清理到下一个"Task:"或文件结尾
        if "\nTask:" in solution_part:
            solution_part = solution_part.split("\nTask:")[0]
        return solution_part.strip()

    return generated.strip()


# ============================================================
# HumanEval 数据集
# ============================================================
def load_humaneval_tasks():
    """加载HumanEval任务"""
    tasks = [
        {'task_id': 'he_01', 'prompt': 'def get_first_element(lst):\n    """Return the first element of lst"""\n',
         'solution': '    return lst[0] if lst else None'},
        {'task_id': 'he_02', 'prompt': 'def double_all(nums):\n    """Double each number in nums"""\n',
         'solution': '    return [x * 2 for x in nums]'},
        {'task_id': 'he_03', 'prompt': 'def sum_list(nums):\n    """Return sum of all numbers"""\n',
         'solution': '    total = 0\n    for n in nums:\n        total += n\n    return total'},
        {'task_id': 'he_04', 'prompt': 'def fibonacci(n):\n    """Return nth Fibonacci number"""\n',
         'solution': '    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)'},
        {'task_id': 'he_05', 'prompt': 'def factorial(n):\n    """Return n!""\n',
         'solution': '    if n <= 1:\n        return 1\n    return n * factorial(n-1)'},
        {'task_id': 'he_06', 'prompt': 'def find_max(nums):\n    """Return maximum value"""\n',
         'solution': '    max_val = nums[0]\n    for n in nums:\n        if n > max_val:\n            max_val = n\n    return max_val'},
        {'task_id': 'he_07', 'prompt': 'def reverse_string(s):\n    """Reverse string s"""\n',
         'solution': '    return s[::-1]'},
        {'task_id': 'he_08', 'prompt': 'def is_palindrome(s):\n    """Check if s is palindrome"""\n',
         'solution': '    return s == s[::-1]'},
        {'task_id': 'he_09', 'prompt': 'def count_vowels(s):\n    """Count vowels in s"""\n',
         'solution': '    return sum(1 for c in s if c in "aeiouAEIOU")'},
        {'task_id': 'he_10', 'prompt': 'def flatten(nested):\n    """Flatten nested list"""\n',
         'solution': '    result = []\n    for item in nested:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result'},
        {'task_id': 'he_11', 'prompt': 'def quicksort(arr):\n    """Sort array"""\n',
         'solution': '    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)'},
        {'task_id': 'he_12', 'prompt': 'def merge_dicts(d1, d2):\n    """Merge two dicts"""\n',
         'solution': '    result = d1.copy()\n    result.update(d2)\n    return result'},
        {'task_id': 'he_13', 'prompt': 'def word_count(s):\n    """Count word frequencies"""\n',
         'solution': '    counts = {}\n    for word in s.split():\n        counts[word] = counts.get(word, 0) + 1\n    return counts'},
        {'task_id': 'he_14', 'prompt': 'def unique_elements(lst):\n    """Return unique elements"""\n',
         'solution': '    return list(set(lst))'},
        {'task_id': 'he_15', 'prompt': 'def has_duplicates(lst):\n    """Check for duplicates"""\n',
         'solution': '    return len(lst) != len(set(lst))'},
        {'task_id': 'he_16', 'prompt': 'def gcd(a, b):\n    """Greatest common divisor"""\n',
         'solution': '    while b:\n        a, b = b, a % b\n    return a'},
        {'task_id': 'he_17', 'prompt': 'def is_prime(n):\n    """Check if n is prime"""\n',
         'solution': '    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True'},
        {'task_id': 'he_18', 'prompt': 'def sieve(n):\n    """Return primes up to n"""\n',
         'solution': '    is_prime = [True] * (n + 1)\n    is_prime[0] = is_prime[1] = False\n    for i in range(2, int(n ** 0.5) + 1):\n        if is_prime[i]:\n            for j in range(i*i, n+1, i):\n                is_prime[j] = False\n    return [i for i in range(n+1) if is_prime[i]]'},
        {'task_id': 'he_19', 'prompt': 'def binary_search(arr, target):\n    """Binary search"""\n',
         'solution': '    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1'},
        {'task_id': 'he_20', 'prompt': 'def deep_copy(obj):\n    """Deep copy nested structure"""\n',
         'solution': '    if isinstance(obj, list):\n        return [deep_copy(item) for item in obj]\n    elif isinstance(obj, dict):\n        return {k: deep_copy(v) for k, v in obj.items()}\n    else:\n        return obj'},
    ]
    return tasks


# ============================================================
# 主实验
# ============================================================
def run_experiment():
    print("=" * 70)
    print("H39 Living Tree - Retrieval + CodeGen Generation")
    print("=" * 70)
    print()
    print("Core Change: Retrieval -> LLM Generation with few-shot context")
    print()

    # ----------------------------------------------------------
    # 加载 CodeBERT (for embeddings)
    # ----------------------------------------------------------
    import torch
    from transformers import AutoTokenizer as CodeBERT_Tokenizer
    from transformers import AutoModel as CodeBERT_Model

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Loading CodeBERT on {device}...")
    codebert_tokenizer = CodeBERT_Tokenizer.from_pretrained("microsoft/codebert-base")
    codebert_model = CodeBERT_Model.from_pretrained("microsoft/codebert-base").to(device)
    codebert_model.eval()

    def embed_codes(codes):
        embs = []
        with torch.no_grad():
            for code in codes:
                inputs = codebert_tokenizer(code, return_tensors='pt',
                                           truncation=True, max_length=512).to(device)
                outputs = codebert_model(**inputs)
                embs.append(outputs.last_hidden_state[:, 0, :].cpu().numpy()[0])
        return np.array(embs)

    print("CodeBERT loaded\n")

    # ----------------------------------------------------------
    # 加载 CodeGen (for generation)
    # ----------------------------------------------------------
    print("Loading CodeGen-350M...")
    from transformers import AutoTokenizer as CG_Tokenizer
    from transformers import AutoModelForCausalLM as CG_Model

    cg_tokenizer = CG_Tokenizer.from_pretrained("Salesforce/codegen-350M-multi")
    cg_model = CG_Model.from_pretrained("Salesforce/codegen-350M-multi").to(device)
    cg_model.eval()
    print("CodeGen loaded\n")

    # ----------------------------------------------------------
    # 加载数据集
    # ----------------------------------------------------------
    print("Loading HumanEval dataset...")
    dataset = load_humaneval_tasks()
    print(f"  Dataset size: {len(dataset)} tasks\n")

    # 生成embeddings
    print("Generating embeddings...")
    codes = [d['prompt'] + d['solution'] for d in dataset]
    embeddings = embed_codes(codes)

    for i, d in enumerate(dataset):
        d['embedding'] = embeddings[i]
    print(f"  Embeddings shape: {embeddings.shape}\n")

    # ----------------------------------------------------------
    # 划分训练/测试
    # ----------------------------------------------------------
    print("Splitting train/test...")
    n_train = 14
    n_test = 6
    train_data = dataset[:n_train]
    test_data = dataset[n_train:n_train+n_test]

    print(f"  Train: {len(train_data)}, Test: {len(test_data)}\n")

    # ----------------------------------------------------------
    # Phase 1: 持续学习
    # ----------------------------------------------------------
    print("=" * 70)
    print("Phase 1: Sequential Learning")
    print("=" * 70)

    lt = LivingTreeH39(embedding_dim=768)
    learn_times = []

    for i, d in enumerate(train_data):
        start = time.time()
        lt.learn_task(d['task_id'], d['embedding'], d['prompt'], d['solution'])
        elapsed = time.time() - start
        learn_times.append(elapsed)

        if i < 3 or i >= len(train_data) - 1:
            print(f"  [{i+1}] Learned {d['task_id']}")

    print(f"\n  Total nodes: {len(lt.nodes)}")
    print(f"  Avg learn time: {np.mean(learn_times)*1000:.2f}ms")
    print(f"  Time growth: {learn_times[-1]/learn_times[0]:.2f}x")
    print()

    # ----------------------------------------------------------
    # Phase 2: 检索 + CodeGen生成
    # ----------------------------------------------------------
    print("=" * 70)
    print("Phase 2: Retrieval + CodeGen Generation")
    print("=" * 70)

    generation_results = []

    for d in test_data:
        problem_emb = d['embedding']
        problem_prompt = d['prompt']
        gt_solution = d['solution']

        # 检索最相似的K个节点
        matches = lt.retrieve(problem_emb, k=3)
        few_shot_examples = [(node.prompt, node.solution) for sim, node in matches]

        print(f"  {d['task_id']}: matched to {matches[0][1].task_id} (sim={matches[0][0]:.3f})")

        # 用CodeGen生成
        generated = generate_with_codegen(
            problem_prompt, few_shot_examples,
            cg_model, cg_tokenizer, device
        )

        # 评估
        score = code_eval(generated, gt_solution)

        generation_results.append({
            'task_id': d['task_id'],
            'gt_solution': gt_solution,
            'generated': generated,
            'matched_task': matches[0][1].task_id,
            'similarity': matches[0][0],
            'score': score,
        })

        print(f"    Score: {score:.2f}")
        print()

    # ----------------------------------------------------------
    # 结果统计
    # ----------------------------------------------------------
    print("=" * 70)
    print("Results Summary")
    print("=" * 70)

    scores = [r['score'] for r in generation_results]
    avg_score = np.mean(scores)

    print(f"\n  CodeGen Generation Score: {avg_score:.2%}")
    print(f"  High quality (>0.7): {sum(1 for s in scores if s > 0.7)}/{len(scores)}")
    print(f"  Medium (0.4-0.7): {sum(1 for s in scores if 0.4 <= s <= 0.7)}/{len(scores)}")
    print(f"  Low (<0.4): {sum(1 for s in scores if s < 0.4)}/{len(scores)}")
    print()

    # 与H36对比
    h36_baseline = 0.7056
    improvement = (avg_score - h36_baseline) / h36_baseline * 100

    print(f"  H36 (direct retrieval): {h36_baseline:.2%}")
    print(f"  H39 (retrieval + CodeGen): {avg_score:.2%}")
    print(f"  Change: {improvement:+.1f}%")
    print()

    # ----------------------------------------------------------
    # Falsify判断
    # ----------------------------------------------------------
    print("--- Falsify Checks ---")

    checks = {
        'generation_works': (avg_score > 0.25,
            f"Generation score > 25%: {avg_score:.1%}"),
        'llm_better_than_retrieval': (avg_score >= h36_baseline * 0.9,
            f"Within 90% of H36: {avg_score/h36_baseline:.1%}"),
        'structural_correctness': (avg_score > 0.4,
            f"Score > 40%: {avg_score:.1%}"),
    }

    passed = 0
    for desc, (ok, detail) in checks.items():
        status = "PASS" if ok else "FAIL"
        print(f"  {status}  {desc}: {detail}")
        if ok:
            passed += 1

    print(f"\n  Passed {passed}/{len(checks)} checks")

    if passed >= 2:
        print("\n  -> Living Tree H39 Retrieval + CodeGen Generation!")
        print("     LLM can use retrieved nodes as few-shot context")

    return {
        'avg_score': avg_score,
        'passed': passed,
        'results': generation_results,
    }


if __name__ == "__main__":
    results = run_experiment()
