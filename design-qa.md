# ClaudeSkills 视觉验收

## Source truth

- Fable 5 终裁：方案 1，技术周刊头版 × 工作台。
- 参考图：`.omx/audits/claudeskills-fable5-v3/04-option-1.png`
- 同屏对照：`.omx/audits/claudeskills-fable5-v3/16-final-desktop-comparison.png`（左为参考，右为实现）
- 移动端没有独立参考图；按 Fable 5 明确的顺序、尺寸和横向导航约束验收。

## Final captures

- 桌面：`.omx/audits/claudeskills-fable5-v3/14-final-desktop-1440x900.png`
- 移动：`.omx/audits/claudeskills-fable5-v3/15-final-mobile-390x844.png`
- 浏览器：Codex in-app browser，设备像素比由浏览器保持默认。

## Checks

| Check | Result |
| --- | --- |
| 1440 × 900 首屏 | 通过；masthead 96px，`01 / 四条主线` 在首屏可见 |
| 390 × 844 首屏 | 通过；masthead 110.77px，页面无横向溢出 |
| 移动端内容顺序 | 通过；masthead → eyebrow → H1 → lede → CTA → 2×2 proof → terminal → section 01 |
| 字体 | 通过；Noto Sans SC 与 JetBrains Mono 均从本地 WOFF2 加载 |
| 锚点 | 通过；“30 秒装一个”到达 `#install`，目标位于 sticky header 下方 |
| 复制 | 通过；安装命令按钮切换为“已复制” |
| FAQ | 通过；首个 disclosure 可展开 |
| Console | 通过；桌面和移动端均无 warning/error |
| 视觉判定 | 94/100；category match，达到 90 分门槛 |
| Fable 5 终验 | 通过，91/100；无 P0、P1、P2 阻塞项 |

## Findings history

1. R4：移动 masthead 为 113.95px，超过 112px 上限；修正移动内边距与 sticky offset。
2. R5：桌面 masthead 含边框为 97px，超过 96px 上限；从最小高度中扣除 1px divider。
3. R6：桌面 96px、移动 110.77px；没有 P0、P1 或 P2 未决项。
4. Fable 5：确认开放 Agent Skills 定位、中文表达与 ChaoGeek 气质均达标，可以上线。
5. 按终验建议关闭代码字体连字，确保 `--depth` 的双连字符按原字符显示。

final result: passed
