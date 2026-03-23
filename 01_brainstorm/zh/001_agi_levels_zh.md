# AGI分级洞见汇总

> 来源：AGI Levels 框架系统性调研
> 整理：FARS 自动科研系统
> 日期：2026-03-23

---

## L1 涌现智能 (Emergent)

**代表**：GPT-2/3/4、Claude、Gemini
**Benchmark**：ImageNet、SST-2（已成熟）

### 核心技术
- Attention / Transformer
- Pre-training + Scaling
- In-context learning

### 核心能力
在训练分布**内**泛化：见过类似的能做好

### 核心瓶颈
- 长尾分布 / 分布外泛化失败
- 缺乏组合泛化（记住见过 → 无法合成未见）
- 幻觉（World Model 不一致）

---

## L2 直觉智能 (Intuitive)

**代表**：GPT-4 + RAG + Tool use
**Benchmark**：VLMEval / GAIA（但测的是任务完成率，**不是** World Model 质量）

### 核心技术
- World Model（世界模型）
- Planning（规划）
- RAG / Tool use

### 核心能力
在训练分布**外**泛化：有目标，能分解子任务

### 核心瓶颈
- 幻觉检测（World Model 与现实不一致）
- World Model 的验证和评估**没有可靠标准**
- 依赖 Prompt Engineering，缺乏物理根基

### 关键洞见
**Benchmark 错位**：VLMEval/GAIA 测任务完成率，但 L2→L3 的 gap 本质是 World Model 质量，不是完成率。
World Model 质量应该用：
- 在未见过的动力学上的预测误差
- 零样本泛化到新任务的能力
- 表征的抽象层级

---

## L3 意图智能 (Intentional)

**代表**：AutoGPT、Voyager、SWE-agent、Devin
**Benchmark**：SWE-bench / HumanEval（有，但衡量任务完成，不是 World Model 质量）

### 核心技术
- Meta-Learning（元学习）
- Self-Evolution（自主进化）
- 自主规划和探索

### 核心能力
学习如何学习；在**训练完全未覆盖**的复杂任务上自主探索

### Devin 关键数据（2024）
- SWE-bench: Devin 13.86% vs GPT-4 3.97%
- HumanEval: Devin 25.22% vs GPT-4 3.97%
- 收益来自**智能体架构**，不是基础模型质量提升

### 核心瓶颈
**Inf Loop（无限循环）是 L3+ 智能体的根本问题**
- 缺乏资源感知：不知道消耗了多少计算资源
- 缺乏自纠正机制：错了无法自主发现
- 缺乏 World Model 评估标准

### 关键洞见
Devin 的收益 = 智能体架构，不是更大的模型
→ L3 的瓶颈是**架构设计**，不是 Scale

---

## L4 反思智能 (Reflexive)

**代表**：Researcher-agent、Scientist-agent
**Benchmark**：不存在

### 核心技术
- Meta-Learning（元学习）
- Self-Correction（元认知自纠正）

### 核心能力
自我改进；学习调整自己的学习策略

### 核心瓶颈
- **多智能体资源感知差**（ChatDev/SWE-agent 无限循环）
- Value Alignment（目标对齐）
- 没有热力学意义的"代价信号"

### 关键洞见
L4 多智能体的瓶颈是**没有计算代价信号**：
- 不知道每个 action 消耗了多少资源
- 没有机制在消耗过大时主动中断
- Landauer 耗散 = 天然的"资源感知信号"

---

## L5 组织智能 (Organizational)

**代表**：尚不存在（2026）
**Benchmark**：不存在

### 核心技术
- Multi-Agent（多智能体）
- Value Alignment（价值对齐）

### 核心瓶颈
- 目标对齐
- 资源分配
- 尚无真正多智能体协作的成功案例

---

## 跨层级关键技术对比

| 层级 | 核心技术 | 缺失 |
|------|----------|------|
| L1 | Attention、Transformer、Scaling | 无法组合泛化 |
| L2 | World Model、Planning | World Model 质量无法评估 |
| L3 | Meta-Learning、Self-Evolution | 无限循环、资源感知缺失 |
| L4 | Multi-Agent、Alignment | 无资源代价信号 |

---

## 核心洞见：System 1 vs System 2

- **System 1**（L1）：快速、自动、无意识 = Attention / 模式匹配
- **System 2**（L3）：缓慢、有意识、逻辑 = World Model + Planning + Meta-Learning

L2→L3 = 从"直觉匹配"到"有意图规划"的跳跃
障碍：**没有物理根基**，全是 Prompt 工程

---

## 核心洞见：训练 Scaling vs 推理 Scaling

| | 训练 Scaling | 推理 Scaling |
|---|---|---|
| 代表 | GPT-3 (Chinchilla) | OpenAI o1 |
| 核心 | compute-optimal | more inference = better reasoning |
| 定律 | LLM scaling law | Inference scaling law（不同！） |

---

## 核心洞见：能耗对比

| 系统 | 能耗 |
|------|------|
| 人脑 | ~20W |
| Claude 对话 | ~3Wh/次 |
| Google AI 总计 | 人脑的10倍 (~200W) |
| LLM 一次训练 | 数百千瓦/次 |

**关键洞见**：Inf Loop = 无限能耗流失
缺乏资源感知 → L3+ 智能体可能在无效循环中浪费大量算力

---

## 核心洞见：具身认知

**具身假说**：物理交互产生更稳定的 World Model

- 具身 AI：World Model 更可靠，但**能耗极高**
- 数字 AI：能耗低，但 World Model 依赖语言先验

**核心问题**（与我们的研究直接相关）：
> 在能耗约束下，具身频率和 World Model 精度是否存在 **Pareto 最优**？

用热力学建模：
- 具身交互 = 降低自由能梯度
- 每次交互 = Landauer 耗散成本
- Pareto 前沿 = 自由能最小化 + 耗散最小化的平衡点

---

## 核心洞见：模块化是AGI的基础

**为什么模块化不可或缺**：
1. **知识组织**：模块化使复杂知识系统化
2. **并行开发**：独立模块可单独迭代
3. **专业化优化**：每个模块可针对性提升
4. **可解释性**：模块边界 = 因果边界

→ 这正是 Paper 3（组件库）的核心论点：
Landauer门 + Hopfield + 互补门 + 路由 = 模块化的热力学实现

---

## 与我们热力学框架的对应

| AGI层级 | 热力学解释 |
|---------|-----------|
| L1 | 自由能 landscape 的吸引子 basin |
| L2 | 吸引子之间的 basin 边缘（组合泛化失败点）|
| L3 | 吸引子之间的鞍点跃迁（需要 World Model 导航）|
| L4 | 曲率感知触发的 MetaGate 自省 |
| L5 | 多吸引子系统的同步与竞争 |

| 我们解决的问题 | AGI框架中的位置 |
|---------------|----------------|
| World Model 质量评估 | L2→L3 gap 的核心 |
| 注意力 = 物理近似 | L1 的物理论证 |
| MetaGate 曲率自省 | L4 的资源感知机制 |
| Landauer 耗散 | 所有层级的计算代价信号 |
| NCA 计算结构迁移 | L2→L3 的物理解释 |
