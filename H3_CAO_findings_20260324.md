# H3 CAO实验发现 (2026-03-24)

## 核心发现

### CAO双刃剑效应
- **StageB（能量景观任务）**: CAO有效——能量方差降低32%，收敛epoch从5→1 ✅
- **Few-shot adaptation（低信号任务）**: CAO**有害**——每步负增益(-0.003)，差于baseline(+0.021) ❌

### 原因分析
CAO的eff_lr = base_lr / (1 + α × curvature)
- 在高曲率+高信号时：curvature反映真实loss landscape曲率，CAO有效
- 在噪声主导时：梯度方差大→curvature被高估→eff_lr降至接近0→学习停滞

### Stage0/StageA INCONCLUSIVE
- Hopfield与baseline在轻量合成任务上几乎无差异（cos_sim差<0.001）

## 实验配置
- Few-shot: 5-way 2-shot, 50 episodes, 3 adaptation steps
- 所有条件准确率≈随机猜测(0.20)——任务本身无结构

## 结论
CAO需要满足：信号充足+曲率高(真实反映loss landscape)。噪声任务中反而有害。
