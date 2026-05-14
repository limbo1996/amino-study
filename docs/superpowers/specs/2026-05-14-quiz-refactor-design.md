# Quiz 模式重构设计

## 目标
将测验模式从「展示分子式图片 + 文本输入判断」改为「展示中文名（英文名）+ 四选一缩写选项」。

## 当前行为
- 展示氨基酸分子式图片
- 用户手动输入三字母/单字母缩写
- 点击 Reveal 判断对错

## 新行为
1. 题目展示：`中文名（英文名）`，不展示图片
2. 四个选项：均为三字母缩写或均为单字母缩写，格式**每题随机**，保证同一题内格式统一
3. 移除文本输入判断功能
4. 用户点击选项后 → 显示对错反馈（✓/✗）+ 结构式图片（fig/*.png）+ 「下一题」按钮
5. 点击「下一题」进入下一题

## 改动范围

### 1. `app/services/quiz.py`
- `generate_abbr_question()` 改为每题独立随机选择 `abbr1` 或 `abbr3` 格式
- 选项 prompt 改为 `f"{name_cn}（{name_en}）"`
- 移除 per-session 统一格式的概念

### 2. `app/services/session.py`
- `build_session()` 中移除 session 级别的格式随机选择，每题由 quiz 层独立决定格式
- question 数据结构调整，每题自带 `format` 字段
- `record_session_answer()` 保持不变

### 3. `app/screens/study_screen.py` + `app/main.py`
- 移除文本输入框
- 改为 4 个选项按钮（A/B/C/D 标签），水平两行或垂直排列
- 点击选项后：
  - 禁用所有选项按钮（防止重复点击）
  - 显示对错状态（正确=绿色 ✓，错误=红色 ✗）
  - 显示结构式图片
  - 显示「下一题」按钮
- 答案在点击选项时自动记录（`submit_answer()`）
- 点击「下一题」触发 `advance()` 进入下一题
- 最后一题完成后显示完成小结

### 4. 测试更新
- `test_quiz_service.py`：验证每题格式随机独立、prompt 格式为 `中文名（英文名）`
- `test_session_service.py`：适配 question 结构变化（每题独立 format）
- `test_study_screen.py`：覆盖选项按钮渲染、对错反馈展示、下一题流程

## 不改动
- 数据库 schema（amino_acids / learning_state / daily_plan）
- 调度逻辑（scheduler.py、plan.py）
- 统计/设置界面
- 重置功能
- 数据加载与启动初始化
