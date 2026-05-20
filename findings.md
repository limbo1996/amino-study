# 发现与决策

## 需求
- Android 学习 App，单人使用，数据本地
- 记忆 20 种氨基酸：中文名、英文名、三字母/单字母缩写、结构式图片
- 闪卡 + 测验（选择题 + 填空）
- 每日新学固定 5 个
- 复习按艾宾浩斯：1/2/4/7/15 天
- 错题优先
- 可重置学习进度

## 研究发现
- 数据源：deepseek_csv_20260513_f1933c.csv（5 列，含图片路径）
- 图片路径规则：/Users/limbo/Project/aa_learn/fig/<单字母>.png
 - Android 运行需要将可写数据放在 App.user_data_dir，资源建议首次启动复制到该目录
 - 当前无法使用 adb/logcat，需在启动时写 crash.log 进行离线诊断
 - 需要最小 Kivy APK 验证 Android 16 + 天玑 9500 运行时可用性
 - 若最小 APK 仍闪退，需尝试仅 arm64-v8a 架构打包
 - 模拟器闪退已定位：Label.font_name 传入 None 会触发 ValueError
 - 计划打包 Noto Sans SC 并统一 font_name 兜底
- Layout bug 根因：show_answer_area/hide_answer_area 动态修改 size_hint_y → Kivy BoxLayout 在 Android 上重布局导致子控件位置错乱（题目消失、选项跑位）
- 解决方案：固定 size_hint_y 比例，仅用 opacity 切换可见性，永不动态改 size_hint_y
 - buildozer.spec 目前仅 include fig/*.png 和 CSV，字体需加入 include_patterns 才会打包
 - 当前字体资源位于 skills 目录，已被 buildozer 排除

## 规划要点
- 项目目录：app/（入口与配置）、app/screens（闪卡/测验/统计/设置）、app/services（调度/出题）、app/data（CSV 导入）、app/db（SQLite）、assets/、fig/、tests/
- 数据表：amino_acids、learning_state、daily_plan
- 开发计划：数据导入与 DB → 调度/出题逻辑 → UI → 测试与打包

## 技术决策
| 决策 | 理由 |
|------|------|
| Kivy + SQLite | 仅 Python 环境，满足本地数据与 UI 需求 |
| 目录结构分层（screens/services/db/data） | 便于维护 UI 与逻辑边界 |
| Android 采用 user_data_dir + 资源复制 | 避免 APK 只读路径导致启动崩溃 |

## 遇到的问题
| 问题 | 解决方案 |
|------|---------|
|      |         |

## 资源
- deepseek_csv_20260513_f1933c.csv
- fig/*.png

## 视觉/浏览器发现
- 无

---
*每执行2次查看/浏览器/搜索操作后更新此文件*
*防止视觉信息丢失*
