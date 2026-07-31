# ClaudeSkills README、官网与宣传素材验收记录

日期：2026-07-31（Asia/Shanghai）

## 结论

本轮 README、GitHub Pages 中英文官网和微信群宣传素材已完成并发布。四条重点 Skill 的确定性合同测试全部通过；线上页面已在真实浏览器中复核。

这些结果证明仓库内的结构、脚本、固定夹具、失败边界和页面交互满足本轮合同，不代表任意未来模型输出都达到同样质量，也不代表真实图片供应商或微信公众号发布已经验证。

## 基线与外部协作

- 源码基线：`f7640f208bffaa2c1e4e7184dd7fc10d6e07f2b9`
- 实现提交：`a8b50454f493bad65f44155f89f4c7220f2b8633`
- 初始源码包：1,125,484 bytes
- 初始源码包 SHA-256：`0D3BCADFF5631889CD6F2AB43AA4BF1FECA232D086843DA86E59D9A42459164D`
- README 定向复核包：33,171 bytes
- README 定向复核包 SHA-256：`292F5F0035EFCCBA437371609302F12B4CDF3C2F15DFC4BD465F2DD370B5C44E`
- 两个源码包上传前密钥扫描：0 命中
- ChatGPT Pro（Skill 研究）：https://chatgpt.com/c/6a6b7531-368c-83ea-be03-84bd7a254054
- ChatGPT Pro（README / Pages）：https://chatgpt.com/c/6a6b7cf1-5de8-83ea-bdc4-de7d91a2589c

ChatGPT Pro 的第一版 README 仍以 `Geek Skills` 为主品牌，并弱化了两项已验证能力，因此没有直接采用。反馈后，它补回并收紧了以下合同：

- Product Manager 的 `grill-me-to-doc` 必须先读证据、每轮只问一个决策、说明推荐答案和理由、支持恢复、输出 `PRODUCT-DOC`，并在实现批准边界前硬停止。
- WeChat Article Writer 必须明确 `article`、`image-prompts`、`layout`、`full-pipeline` 四种模式；配图清单与供应商无关，提示词不等于成图，流程不自动发布。
- 17 条合同测试不得描述成四条工作流的真实生产 E2E。

## 实际修改

- 重写中英文 README：从质量报告式中段改为“真实输入 → 工作流 → 可检查产物”，把安装命令接到第一条实际调用。
- 重写中英文 GitHub Pages 文案：清理中文翻译腔，统一品牌为 `ClaudeSkills`，强化四条升级主线及能力边界。
- 调整响应式排版：中文主标题在桌面和窄屏均固定为自然的两行，不出现页面级横向溢出。
- 生成 README 横版头图和微信群竖版海报，并保存可复用生图提示词与群发文案。

生成资产：

| 文件 | 尺寸 | 大小 | SHA-256 |
|---|---:|---:|---|
| `assets/claudeskills-readme-hero.png` | 1774 × 887 | 2,298,481 bytes | `C29B69BCABD08451F03A74FA391A7EA542C89DD6F5CE494CE9AAF2B57C84AAA8` |
| `assets/social/claudeskills-update-wechat-20260731.png` | 1086 × 1448 | 2,417,578 bytes | `243A07B1BEB613D6AFD50071710CEE188C8FE333F65B0BC3D9644635EB1052D0` |

## 独立测试

| 检查 | 结果 | 边界 |
|---|---|---|
| `python scripts/validate.py` | PASS，13 个精选 Skill | 结构合同，不是 13 个真实业务 E2E |
| `python scripts/run_routing_evals.py` | PASS，10 个 Skill、91 条定义 | schema、目标、唯一性和冲突；不是模型实际路由准确率 |
| Python 编译 | PASS，13 个文件 | 只证明可解析 |
| Node `--check` | PASS，7 个文件 | 只证明可解析 |
| 夹具完整性 | PASS，固定哈希和 9 个负例错误 | 固定夹具 |
| 四旗舰合同测试 | PASS，17/17 | Product Manager、WeChat、Deep Research、Deck 的确定性路径 |
| Deck 合成 | PASS | 真实 Chromium：HTML → 9 张 PNG → PPTX；不是 Office / LibreOffice 一致性验证 |
| 站点校验 | PASS，2 页、13 个 Skill 链接、Pages workflow | 静态合同 |
| 站点负面夹具 | 按预期 FAIL，35 条错误、退出码 1 | 验证校验器会拒绝坏页面 |
| README 本地链接 | PASS | 本地目标存在 |
| `git diff --check` | PASS | 无空白错误 |

Deck 合同第一次运行时没有继承 Codex 内置 Node 模块路径；补齐后发现 Playwright 包需要 Chromium `1228`，而本机只有旧缓存 `1181`。安装匹配的 headless shell 后，在不修改仓库依赖、锁文件或断言的情况下重跑，最终 17/17 通过。

## 浏览器验收

本地真实浏览器：

- 桌面 1280 × 720、移动端 390 × 844、窄屏 320 × 720 均无页面级横向溢出。
- 中文主标题、四旗舰卡片、安装锚点、中英切换、外链、跳到正文、复制按钮、FAQ 键盘开合均通过。
- 代码块和证据表在窄屏使用自身滚动容器，没有撑破页面。

线上真实浏览器：

- 页面：https://staruhub.github.io/ClaudeSkills/
- 中文页标题、语言属性、单一 H1、最新样式版本、Product Manager 和 WeChat 边界文案均与提交一致。
- 390 × 844 线上复核无页面级横向溢出。

## 发布证据

- GitHub `main`：`a8b50454f493bad65f44155f89f4c7220f2b8633`
- Validation：https://github.com/staruhub/ClaudeSkills/actions/runs/30599459241 （success）
- Pages：https://github.com/staruhub/ClaudeSkills/actions/runs/30599459246 （success）
- 线上地址：https://staruhub.github.io/ClaudeSkills/

## 仍未验证

- 没有对 13 个精选 Skill 全部执行真实模型、真实外部服务和真实用户数据的生产 E2E；本轮深度合同覆盖用户指定的四条重点工作流。
- Deep Research 没有验证外部网络可达性和来源内容在未来日期仍然有效。
- WeChat 没有调用真实生图供应商，也没有登录或发布到微信公众号。
- Deck 没有验证 Office、LibreOffice 和其他演示软件的像素级一致性；生成的 PPTX 以整页栅格图为主，不是逐元素可编辑版式。
- 静态门禁和模型自测都不是第三方认证。
