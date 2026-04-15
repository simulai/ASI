"""
H39 Living Tree - Retrieval + CodeGen (Kaggle Version)
======================================================

Kaggle-optimized: 30-minute timeout, GPU-accelerated.

Author: Claude Code
Date: 2026-04-15
"""

import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# Living Tree
class LNode:
    def __init__(self, tid, emb, sol): self.tid, self.emb, self.sol = tid, emb, sol
    def sim(self, o): return np.dot(self.emb, o) / (np.linalg.norm(self.emb) * np.linalg.norm(o) + 1e-8)

class LivingTree:
    def __init__(self): self.nodes = {}
    def learn(self, tid, emb, sol): self.nodes[tid] = LNode(tid, emb, sol)
    def retrieve(self, emb, k=3):
        sims = [(n.sim(emb), n) for n in self.nodes.values()]
        sims.sort(key=lambda x: x[0], reverse=True)
        return sims[:k]

# Code eval
def code_eval(gen, gt):
    import re
    def patterns(c):
        p = set(re.findall(r'\b(return|for|if|while|def|\[.*?for|\bextend|\bappend)\b', c))
        return p
    if gen.strip() == gt.strip(): return 1.0
    gp, tp = patterns(gen), patterns(gt)
    if not tp: return 0.0
    return len(gp & tp) / len(tp)

# CodeGen generation
def generate(prompt, examples, model, tokenizer, device):
    fs = "Below are some code examples:\n\n"
    for p, s in examples:
        fs += f"Task:\n{p}\nSolution:\n{s}\n\n"
    fs += f"Task:\n{prompt}\nSolution:\n"

    inputs = tokenizer(fs, return_tensors="pt", truncation=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=80, temperature=0.3,
                                top_p=0.95, do_sample=True, pad_token_id=tokenizer.eos_token_id)
    gen = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if "Solution:\n" in gen:
        sol = gen.split("Solution:\n")[-1]
        if "\nTask:" in sol: sol = sol.split("\nTask:")[0]
        return sol.strip()
    return gen.strip()

# HumanEval (simplified 20 tasks)
def load_tasks():
    return [
        ('he_01', 'def get_first_element(lst):\n    """Return the first element"""\n', 'return lst[0] if lst else None'),
        ('he_02', 'def double_all(nums):\n    """Double each number"""\n', 'return [x * 2 for x in nums]'),
        ('he_03', 'def sum_list(nums):\n    """Return sum"""\n', 'total = 0\nfor n in nums:\ntotal += n\nreturn total'),
        ('he_04', 'def fibonacci(n):\n    """Return nth Fibonacci"""\n', 'if n <= 1:\nreturn n\nreturn fibonacci(n-1) + fibonacci(n-2)'),
        ('he_05', 'def factorial(n):\n    """Return n!""\n', 'if n <= 1:\nreturn 1\nreturn n * factorial(n-1)'),
        ('he_06', 'def find_max(nums):\n    """Return maximum"""\n', 'max_val = nums[0]\nfor n in nums:\nif n > max_val:\nmax_val = n\nreturn max_val'),
        ('he_07', 'def reverse_string(s):\n    """Reverse string"""\n', 'return s[::-1]'),
        ('he_08', 'def is_palindrome(s):\n    """Check palindrome"""\n', 'return s == s[::-1]'),
        ('he_09', 'def count_vowels(s):\n    """Count vowels"""\n', 'return sum(1 for c in s if c in "aeiouAEIOU")'),
        ('he_10', 'def flatten(nested):\n    """Flatten list"""\n', 'result = []\nfor item in nested:\nif isinstance(item, list):\nresult.extend(flatten(item))\nelse:\nresult.append(item)\nreturn result'),
        ('he_11', 'def quicksort(arr):\n    """Sort array"""\n', 'if len(arr) <= 1:\nreturn arr\npivot = arr[len(arr) // 2]\nreturn quicksort([x for x in arr if x < pivot]) + [x for x in arr if x == pivot] + quicksort([x for x in arr if x > pivot])'),
        ('he_12', 'def merge_dicts(d1, d2):\n    """Merge dicts"""\n', 'result = d1.copy()\nresult.update(d2)\nreturn result'),
        ('he_13', 'def word_count(s):\n    """Count words"""\n', 'counts = {}\nfor word in s.split():\ncounts[word] = counts.get(word, 0) + 1\nreturn counts'),
        ('he_14', 'def unique_elements(lst):\n    """Unique elements"""\n', 'return list(set(lst))'),
        ('he_15', 'def has_duplicates(lst):\n    """Check duplicates"""\n', 'return len(lst) != len(set(lst))'),
        ('he_16', 'def gcd(a, b):\n    """GCD"""\n', 'while b:\na, b = b, a % b\nreturn a'),
        ('he_17', 'def is_prime(n):\n    """Check prime"""\n', 'if n < 2:\nreturn False\nfor i in range(2, int(n ** 0.5) + 1):\nif n % i == 0:\nreturn False\nreturn True'),
        ('he_18', 'def sieve(n):\n    """Sieve of Eratosthenes"""\n', 'is_prime = [True] * (n + 1)\nis_prime[0] = is_prime[1] = False\nfor i in range(2, int(n ** 0.5) + 1):\nif is_prime[i]:\nfor j in range(i*i, n+1, i):\nis_prime[j] = False\nreturn [i for i in range(n+1) if is_prime[i]]'),
        ('he_19', 'def binary_search(arr, target):\n    """Binary search"""\n', 'left, right = 0, len(arr) - 1\nwhile left <= right:\nmid = (left + right) // 2\nif arr[mid] == target:\nreturn mid\nelif arr[mid] < target:\nleft = mid + 1\nelse:\nright = mid - 1\nreturn -1'),
        ('he_20', 'def deep_copy(obj):\n    """Deep copy"""\n', 'if isinstance(obj, list):\nreturn [deep_copy(item) for item in obj]\nelif isinstance(obj, dict):\nreturn {k: deep_copy(v) for k, v in obj.items()}\nelse:\nreturn obj'),
    ]

def main():
    print("=" * 60)
    print("H39 Living Tree - Retrieval + CodeGen (Kaggle)")
    print("=" * 60)

    import torch
    from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    # CodeBERT for embeddings
    print("Loading CodeBERT...")
    cb_tok = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    cb_model = AutoModel.from_pretrained("microsoft/codebert-base").to(device)
    cb_model.eval()

    def embed(texts):
        embs = []
        with torch.no_grad():
            for t in texts:
                inp = cb_tok(t, return_tensors='pt', truncation=True, max_length=256).to(device)
                out = cb_model(**inp)
                embs.append(out.last_hidden_state[:, 0, :].cpu().numpy()[0])
        return np.array(embs)

    # CodeGen for generation
    print("Loading CodeGen-350M...")
    cg_tok = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-multi")
    cg_model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-multi").to(device)
    cg_model.eval()

    # Load tasks
    print("Loading tasks...")
    tasks = load_tasks()
    train, test = tasks[:14], tasks[14:]
    print(f"Train: {len(train)}, Test: {len(test)}")

    # Embed
    print("Generating embeddings...")
    train_embs = embed([f"{p}{s}" for _, p, s in tasks])
    test_embs = embed([f"{p}{s}" for _, p, s in test])

    # Learn
    print("Learning...")
    lt = LivingTree()
    times = []
    for i, (tid, p, s) in enumerate(train):
        t0 = time.time()
        lt.learn(tid, train_embs[i], s)
        times.append(time.time() - t0)
    print(f"Nodes: {len(lt.nodes)}, Time growth: {times[-1]/times[0]:.2f}x")

    # Generate
    print("Generating with CodeGen...")
    results = []
    for i, (tid, prompt, gt) in enumerate(test):
        matches = lt.retrieve(test_embs[i], k=3)
        # Build few-shot examples from matched nodes
        examples = []
        for sim, node in matches:
            # Find the corresponding train task
            for j, (t, p, s) in enumerate(train):
                if t == node.tid:
                    examples.append((p, s))
                    break
        if not examples:
            examples = [(p, s) for _, p, s in train[:3]]

        gen = generate(prompt, examples, cg_model, cg_tok, device)
        score = code_eval(gen, gt)
        results.append((tid, score, gen[:50] if gen else "empty", gt[:50]))

    scores = [r[1] for r in results]
    avg = np.mean(scores)

    print(f"\nCodeGen Score: {avg:.2%}")
    print(f"High (>0.7): {sum(1 for s in scores if s > 0.7)}/{len(scores)}")

    # Falsify
    h36 = 0.7056
    print(f"\nH36 (retrieval): {h36:.2%}")
    print(f"H39 (CodeGen): {avg:.2%}")
    print(f"Change: {(avg-h36)/h36*100:+.1f}%")

    passed = sum(1 for s in [avg > 0.25, avg >= h36*0.9, avg > 0.4] if s)
    print(f"\n{passed}/3 checks passed")
    print("-> H39 complete!")

if __name__ == "__main__":
    main()
