# my-openclash-rule

个人 OpenClash / subconverter 规则仓库，用于维护一份精简、可审计的远程订阅转换配置。目标是保证 AI、科研检索、GitHub、账号登录等场景稳定，不追求复杂流媒体分流或强广告拦截。

## 仓库结构

- `qichiyu_original.ini`：qichiyu 原始配置，仅作参考，不直接使用。
- `openclash_personal.ini`：个人精简版订阅转换主配置，供 OpenClash / subconverter 使用。
- `rules/Direct.list`：强制直连规则。
- `rules/ProxyLite.list`：强制代理规则。
- `rules/AI.list`：AI 服务分流规则。
- `rules/Claude.list`：Claude / Anthropic 专用规则。
- `scripts/check_rules.py`：规则格式检查脚本。

## OpenClash 使用方式

将仓库推送到 GitHub 后，在 OpenClash 订阅转换远程配置中使用：

```text
https://raw.githubusercontent.com/USERNAME/my-openclash-rule/main/openclash_personal.ini
```

初始化阶段配置中的 `USERNAME` 是占位符。确认仓库路径后再替换为自己的 GitHub 用户名。

## 维护规则

添加强制直连规则：编辑 `rules/Direct.list`，例如国内站点、校园站点、银行、Apple 登录相关补充域名。

添加强制代理规则：编辑 `rules/ProxyLite.list`，用于需要稳定代理但不属于更细服务组的域名。

添加普通 AI 规则：编辑 `rules/AI.list`，用于 OpenAI、ChatGPT、Codex、Gemini、Perplexity、Cursor 等非 Claude 服务。

添加 Claude 专用规则：编辑 `rules/Claude.list`。Claude 网页、Claude Code、Anthropic API 和相关依赖放在这里，并在主配置中早于普通 AI 规则引用。

Claude 单独走 `🧠 Claude固定家宽`，第一版固定匹配 `BGP智能路由-美国07-家宽-ss-x2`。这样避免 Claude 被普通 AI、Google、ProxyGFWlist 或 FINAL 抢走，也避免 fallback、load-balance、自动测速切换造成账号环境漂移。

Apple 默认 `DIRECT`，用于减少 App Store、Apple ID、iCloud 登录和设备验证异常。

`🐟 漏网之鱼` 默认 `DIRECT`，用于降低未知国内站点、学校系统、验证码、支付页面误走代理的概率。需要代理的域名应显式加入 `rules/ProxyLite.list` 或对应服务规则。

流媒体和广告规则默认注释。Netflix、TikTok、国外媒体、BanAD、BanProgramAD 等模板保留在配置里，未来需要时再手动取消注释并检查影响。

## 检查

运行：

```bash
python3 scripts/check_rules.py
```

脚本会检查 `.list` 重复规则、异常空行、非法规则类型、URL 误写为 `DOMAIN-SUFFIX`、敏感信息、主配置引用的本地规则文件、Claude/AI 顺序和广告 ruleset 是否仍处于注释状态。初始化阶段 `USERNAME` 占位符只会产生 warning。

## 安全原则

不要提交任何真实订阅链接、真实节点信息、proxy-providers URL、token、password、passwd、secret、bearer，或 `ss://`、`ssr://`、`vmess://`、`vless://`、`trojan://`、`hysteria://`、`hy2://` 链接。
