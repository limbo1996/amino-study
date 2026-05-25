# 任务计划：在题目中显示氨基酸「性质」

## 目标
在 quiz 题目中，将 CSV 中的「性质」列以第二行的形式展示在氨基酸名称下方，第一行字号64，第二行字号28。

## 当前阶段
阶段 2

## 各阶段

### 阶段 1：需求与发现 ✅
- [x] 理解用户意图
- [x] 确定约束条件和需求
- [x] 将发现记录到 findings.md
- **状态：** complete（已在 brainstorming 阶段完成）

### 阶段 2：规划与结构
- [ ] 确定技术方案
- [ ] 确认所有改动文件和顺序
- [ ] 记录决策及理由
- **状态：** in_progress

### 阶段 3：实现
- [ ] 按 TDD 流程编写测试 → 实现代码
- [ ] 先写测试，再写实现
- [ ] 增量测试
- **状态：** pending

### 阶段 4：测试与验证
- [ ] 运行所有测试确保无回归
- [ ] 将测试结果记录到 progress.md
- [ ] 修复发现的问题
- **状态：** pending

### 阶段 5：交付
- [ ] Ralph 确认
- [ ] Git commit
- [ ] 交付给用户
- **状态：** pending

## 关键问题
（已全部在 brainstorming 中解决）

## 已做决策
| 决策 | 理由 |
|------|------|
| 新增 `nature` 列而非复用 `formula` | 语义清晰、有迁移先例、保留扩展性 |
| 使用 Kivy markup 模式而非拆分 Label | 不改 widget 层级，避免 Android `size_hint_y` 风险 |
| 进度保持在第一行 | 用户选择 A |
| 性质不带前缀标签 | 用户选择 A |
| 字号 64/28 | 用户选择方案 C |

## 遇到的错误
（暂无）

## 备注
- 严格按 AGENTS.md 流程：brainstorming → planning → TDD → ralph → commit
- 改动顺序：CSV loader → DB migration → session → UI
- Kivy 约束：不改 `size_hint_y`，不用 `None` 给 `font_name`
