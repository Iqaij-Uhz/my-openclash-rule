# Changelog

## 2026-06-17 Round 1

- 修正 AI / Claude 规则分离，普通 AI 不再默认包含 Claude / Anthropic。
- 将 `auth0`、`intercom`、`sentry` 等通用第三方服务改为 AI 注释模板，避免误分流。
- 将 Claude 里的 `sentry.io` 改为注释模板，仅在确认 Claude Code 需要时启用。
- 新增 `rules/Payment.list` 和 `💳 支付服务` 策略组，支付规则独立于 Claude / AI。
- 新增 `rules/PhoneClaude.list`，让 iPhone `192.168.5.50` 的公网流量走 Claude 固定家宽。
- 调整 ruleset 顺序，使 `LocalAreaNetwork.list` 早于 `PhoneClaude.list`，保证局域网访问直连。
- 删除 `qichiyu_original.ini`，仓库仅保留正式使用的 `openclash_personal.ini`。
- 更新 `scripts/check_rules.py`，增加 PhoneClaude、Payment、规则顺序和规则隔离检查。
- 更新 `README.md`，补充支付、iPhone 分流和 Claude 固定家宽说明。

## 2026-06-17

- 新增 `openclash_personal.ini`，基于 qichiyu 原始配置精简为个人 OpenClash / subconverter 配置。
- 新增 `rules/Claude.list`，将 Claude / Anthropic 流量固定到专用美国家宽策略组。
- 更新 `rules/AI.list`，移除 Claude / Anthropic 规则，补充常见非 Claude AI 服务。
- 清理 `rules/Direct.list` 和 `rules/ProxyLite.list` 中的重复规则。
- 新增 `scripts/check_rules.py`，用于检查规则重复、格式、敏感信息、引用文件、规则顺序和广告规则状态。
- 更新 `README.md`，补充仓库用途、结构、OpenClash 使用方式、维护方法和安全原则。

## 2026-06-16

- 初始化个人 OpenClash 规则仓库。
- 添加 qichiyu 原始配置备份。
- 添加 Direct.list、ProxyLite.list、AI.list。
