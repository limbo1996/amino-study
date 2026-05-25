# 发现与决策

## 需求
- CSV 中新增了「性质」列，包含氨基酸的电荷/极性信息
- 需要在题目下方以更小字号显示
- 第一行字号保持64（不变），第二行字号28
- 进度条保持在第一行
- 性质不带前缀标签

## 研究发现

### CSV 现状
- `deepseek_csv_20260513_f1933c.csv` 有 6 列：中文名、英文名、三字缩写、单字缩写、图片路径、性质
- 性质值有 5 类：非极性脂肪族、碱性（带正电）、极性不带电、酸性（带负电）、芳香族
- 现有 loader 的 `REQUIRED_FIELDS` 只有前 5 列，读取的 `分子式` 列不存在

### 数据流
```
CSV (性质列) → loader.py (未读取) → DB amino_acids.formula (始终为"")
                                                    ↓
                                            session.py → question dict → UI
```
- `formula` 字段从 loader 到 DB 到 session 到 UI 整个链路都存在但值始终为空

### Kivy Label 限制
- 普通 Label 只支持单一字号
- 实现多种字号需要 `markup=True` + `[size=XX]` 标签
- 需要对文本中的 `[` 和 `]` 做转义

### 已有迁移模式
- `migrate_add_daily_streak()` 示范了 `ALTER TABLE ADD COLUMN` + `sqlite3.OperationalError` 捕获的幂等迁移

## 技术决策
| 决策 | 理由 |
|------|------|
| 新增 `nature` 列而非复用 `formula` | 语义清晰、保留扩展性 |
| Kivy markup 模式 | 单 Label 不改层级，避免 Android `size_hint_y` bug |
| 转移 scheme：`[`→`&bl;` `]`→`&br;` | Kivy markup 的 BBcode 转义规则 |
| `ALTER TABLE ADD COLUMN` 带默认值 | 保持与现有 streak 迁移一致的模式 |

## 视觉/浏览器发现
- 用户通过浏览器 mockup 选择了方案 C：字号 64/28 搭配
- 方案 A (72/36) 和方案 B (80/40) 被否决
- 方案 C 实际第一行字号与当前一致（64），第二行为 28

---
*每执行2次查看/浏览器/搜索操作后更新此文件*
