# 氨基酸记忆 Android 应用设计

## 背景与目标
该应用用于在碎片化时间记忆 20 种蛋白质氨基酸的中文名、英文名、三字母缩写、单字母缩写与结构式图片。仅单人使用，数据本地保存，支持闪卡与测验，错题优先复习，按艾宾浩斯 1/2/4/7/15 天安排复习，支持一键重置学习进度。

## 范围
- 平台：Android
- 技术：Python + Kivy
- 数据：本地 SQLite
- 数据源：deepseek_csv_20260513_f1933c.csv（20 条）
- 结构式图片：fig/<单字母>.png

## 方案与权衡
推荐方案：Kivy + SQLite。

理由：满足“仅用 Python”的约束，SQLite 适合本地小数据量，复习调度与错题优先需要可查询与更新的数据结构。

## 架构与组件
1. 数据层：SQLite + CSV 导入
2. 业务层：学习调度（复习间隔 + 错题优先）与出题策略
3. UI 层：闪卡、测验、统计、设置

### 目录结构
- app/
  - main.py（入口）
  - screens/（闪卡、测验、统计、设置）
  - services/（调度、出题、进度）
  - data/（CSV 导入与校验）
  - db/（数据库初始化与访问）
- assets/（图标、字体、背景）
- fig/（结构式图片）
- tests/（逻辑单测）

## 数据模型

### amino_acids
- id INTEGER PK
- name_cn TEXT
- name_en TEXT
- abbr3 TEXT
- abbr1 TEXT
- image_path TEXT

### learning_state
- id INTEGER PK
- amino_id INTEGER FK -> amino_acids.id
- status TEXT (new/learning/reviewed/mastered)
- last_seen_at DATETIME
- next_review_at DATETIME
- wrong_count INTEGER
- right_streak INTEGER

### daily_plan
- id INTEGER PK
- plan_date DATE
- new_quota INTEGER (固定 5)
- new_done INTEGER
- review_done INTEGER

## 学习与复习逻辑
1. 每日新学固定 5 个。
2. 复习间隔使用 1/2/4/7/15 天。
3. 题目生成优先复习到期题，且错题优先（按 wrong_count 与到期时间排序）。
4. 当日流程：先复习，再新学。
5. 重置：清空 learning_state 与 daily_plan，恢复为未学习状态。

## 测验题型
- 选择题：四选一，干扰项从同字段随机抽取
- 填空题：输入英文名/缩写/化学式等字段
- 字段轮换：题干与答案字段随机组合，避免单一记忆路径

## 测试策略
- 逻辑单测：复习间隔计算、错题优先排序、每日新学配额、重置逻辑
- 运行验证：首次导入 20 条数据，启动后可生成当日计划

## 风险与约束
- 仅用 Python：包体可能较大
- 结构式图片由用户提供，需确保路径有效

## 交付物
- 目录结构与核心逻辑
- SQLite 数据库
- Kivy UI
- 单元测试
