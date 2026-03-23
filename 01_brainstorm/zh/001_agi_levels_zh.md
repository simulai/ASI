# AGI 各版本总结

> 来源：AGI Levels 框架系统性调研
> 日期：2026-03-23
> 整理：FARS 自动科研系统

## AGI Level 0: 无智能
没有任何智能行为。

## AGI Level 1: 涌现Emergent
被动响应，无目标保持。
例：线性回归、传统ML、基础搜索引擎

## AGI Level 2: 直觉Intuitive
模式匹配+记忆，涌现行为。
 Benchmark成熟：ImageNet、SST-2等
代表：GPT-2/3/4、Claude、Gemini

**核心能力**：在训练分布内泛化
**核心瓶颈**：无法可靠合成新规则

## AGI Level 3: 意图Intentional
目标分解、长期规划、主动探索。
 Benchmark缺失：VLMEval/GAIA测任务完成率，不测世界模型质量
代表：AutoGPT、Voyager、SWE-agent

**核心能力**：在训练分布外泛化
**核心瓶颈**：缺乏物理论证，主要靠prompt工程

## AGI Level 4: 反射Reflexive
学习如何学习，元认知。
 Benchmark：无从谈起
代表：Researcher-agent、Scientist-agent

**核心能力**：自我改进
**核心瓶颈**：多智能体资源感知差（无限循环）

## AGI Level 5: 组织Organizational
多智能体协作、涌现组织。
**核心瓶颈**：目标对齐、资源分配

---

## 各层级核心技术

| Level | 核心机制 | 缺失 |
|--------|----------|------|
| L1 | 记忆、涌现 | 无规划 |
| L2 | Attention、Transformer | 无目标保持 |
| L3 | World Model、Planning | 无物理基础 |
| L4 | Meta-Learning、元认知 | 无资源感知 |
| L5 | 多智能体、对齐 | 无理论框架 |

---

## 关键发现

1. **L2→L3是最大的gap**：从"记住"到"合成"，需要组合泛化
2. **L3的世界模型评估是空白**：没有benchmark衡量世界模型本身质量
3. **L4多智能体的资源瓶颈**：ChatDev/SWE-agent会无限循环，没有热力学意义的"代价信号"
4. **具身AI vs 数字AI**：物理交互产生更稳定的世界模型，但能耗高

---

## 与我们的热力学框架的对应

- L2 = 自由能 landscape 的**吸引子 basin**
- L3 = 吸引子之间的**鞍点跃迁**
- L4 = 曲率感知触发的**元认知**
- L5 = 多吸引子系统的**同步与竞争**

Landauer耗散 = 每个层级的**计算代价信号**
