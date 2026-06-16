# Changelog

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
