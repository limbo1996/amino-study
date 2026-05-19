# 任务计划：氨基酸记忆 Android 应用

## 目标
使用 Kivy + SQLite 构建本地单人学习 App，支持闪卡与测验、错题优先与艾宾浩斯复习、每日新学 5 个、可重置进度。

## 当前阶段
阶段 7

## 各阶段

### 阶段 1：需求与发现
- [x] 确认数据源与图片路径
- [x] 固定学习与复习规则
- [x] 将发现记录到 findings.md
- **状态：** complete

### 阶段 2：规划与结构
- [x] 确定项目目录与数据库结构
- [x] 写入计划与决策
- **状态：** complete

### 阶段 3：实现
- [x] 编写调度逻辑的测试（RED）
- [x] 实现最小调度逻辑（GREEN）
- [x] 编写应用入口测试（RED）
- [x] 实现最小应用入口（GREEN）
- [x] 编写 CSV 导入测试（RED）
- [x] 实现 CSV 导入逻辑（GREEN）
- [x] 编写 SQLite 初始化与导入测试（RED）
- [x] 实现 SQLite 初始化与导入逻辑（GREEN）
- [x] 编写启动初始化测试（RED）
- [x] 实现启动初始化接入（GREEN）
- [x] 初始化项目结构与数据层
- [x] 编写学习调度持久化测试（RED）
- [x] 实现学习调度持久化逻辑（GREEN）
- [x] 编写计划构建测试（RED）
- [x] 实现计划构建逻辑（GREEN）
- [x] 编写出题逻辑测试（RED）
- [x] 实现出题逻辑（GREEN）
- [x] 编写学习会话服务测试（RED）
- [x] 实现学习会话服务（GREEN）
- [x] 编写计划计数更新测试（RED）
- [x] 实现计划计数更新逻辑（GREEN）
- [x] 实现学习调度与出题逻辑
- [x] 编写学习界面测试（RED）
- [x] 实现学习界面最小 UI（GREEN）
- [x] 编写学习图片展示测试（RED）
- [x] 实现学习图片展示（GREEN）
- [x] 编写统计/设置界面测试（RED）
- [x] 实现统计/设置界面最小 UI（GREEN）
- [x] 编写重置服务测试（RED）
- [x] 实现重置服务并接入UI（GREEN）
- [x] 实现 Kivy UI（闪卡/测验/统计/设置）
- **状态：** complete

### 阶段 4：测试与验证
- [x] 运行单元测试
- [x] 验证规则：每日新学 5 + 艾宾浩斯 + 错题优先 + 重置
- [x] 记录测试结果到 progress.md
- **状态：** complete

### 阶段 5：交付
- [ ] 确认文件清单与文档
- [ ] 交付并说明后续步骤
- **状态：** pending

### 阶段 6：Quiz 模式重构
- [x] 改造 quiz.py 出题逻辑：每题独立随机 abbr1/abbr3，prompt 改为中文名（英文名）
- [x] 改造 session.py 会话编排：移除 session 级格式选择
- [x] 改造 study_screen.py + main.py UI：移除输入框，新增 4 选项按钮 + 对错反馈 + 结构式图片 + 下一题
- [x] 更新测试：quiz 测试、session 测试、study_screen 测试
- [x] 运行全量测试验证
- **状态：** complete

### 阶段 7：Android 路径与资源修复
- [x] 设计：DB 迁移至 user_data_dir，资源首次启动复制
- [x] 更新配置与加载逻辑（DB/CSV/图片路径）
- [x] 更新 Buildozer 打包资源配置
- [x] 补充/更新测试
- [x] 运行测试并记录结果
- **状态：** complete

## 关键问题
1. 无

## 已做决策
| 决策 | 理由 |
|------|------|
| 采用 Kivy + SQLite | 仅用 Python，数据本地，满足需求 |
| 数据源使用 deepseek_csv_20260513_f1933c.csv | 用户已提供完整 20 种数据 |
| 结构式图片使用 fig/*.png | 用户已提供并命名规则明确 |

## 遇到的错误
| 错误 | 尝试次数 | 解决方案 |
|------|---------|---------|
| session-catchup.py 路径缺失 | 1 | 记录为已知环境问题，继续手动更新规划文件 |

## 备注
- 每次修改必须先 brainstorming，再 planning-with-files-zh，再 test-driven-development，结束后 ralph 确认。
- 每次修改必须提交 git。
