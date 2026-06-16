# my-openclash-rule

个人 OpenClash / subconverter 规则仓库，用于维护一份精简、可审计的远程订阅转换配置。目标是保证 AI、科研检索、GitHub、账号登录等场景稳定，不追求复杂流媒体分流或强广告拦截。

## 仓库结构

- `openclash_personal.ini`：个人精简版订阅转换主配置，供 OpenClash / subconverter 使用。
- `rules/Direct.list`：强制直连规则。
- `rules/ProxyLite.list`：强制代理规则。
- `rules/AI.list`：AI 服务分流规则。
- `rules/Claude.list`：Claude / Anthropic 专用规则。
- `rules/Payment.list`：支付和账号稳定相关规则。
- `rules/PhoneClaude.list`：iPhone `192.168.5.50` 公网流量专用规则。
- `scripts/check_rules.py`：规则格式检查脚本。

## OpenClash 使用方式

将仓库推送到 GitHub 后，在 OpenClash 订阅转换远程配置中使用：

```text
https://raw.githubusercontent.com/Iqaij-Uhz/my-openclash-rule/main/openclash_personal.ini
```

如仓库名或分支名发生变化，需要同步更新 `openclash_personal.ini` 中引用的 raw 地址。

## 低内存稳定版

当前配置面向内存较小的 OpenClash / Mihomo 运行环境，优先避免规则集过大导致内核 OOM 被系统杀掉。为降低内存压力，暂时关闭：

- `GEOSITE,geolocation-!cn`
- `GEOSITE,CN`
- `ChinaDomain.list`
- `ChinaCompanyIp.list`

当前主要依靠 `ProxyGFWlist`、自定义 AI / Claude / GitHub / Google / Telegram / YouTube / Payment 规则、`GEOIP,CN,no-resolve` 和 `FINAL` 默认直连来保持稳定。需要更强覆盖时，优先少量补充 `rules/Direct.list` 或 `rules/ProxyLite.list`，不要一次性打开大型规则集。

## 维护规则

添加强制直连规则：编辑 `rules/Direct.list`，例如国内站点、校园站点、银行、Apple 登录相关补充域名。

添加强制代理规则：编辑 `rules/ProxyLite.list`，用于需要稳定代理但不属于更细服务组的域名。

添加普通 AI 规则：编辑 `rules/AI.list`，用于 OpenAI、ChatGPT、Codex、Gemini、Perplexity、Cursor 等非 Claude 服务。

添加 Claude 专用规则：编辑 `rules/Claude.list`。Claude 网页、Claude Code、Anthropic API 和相关依赖放在这里，并在主配置中早于普通 AI 规则引用。

Claude 单独走 `🧠 Claude固定家宽`，优先匹配 `BGP智能路由-美国07-家宽-ss-x2`。该组不使用 fallback、load-balance、url-test，目的是避免自动测速切换造成账号环境漂移；同时保留 `🏡 美国家宽备用` 和 `🐸 手动切换` 作为显式兜底，避免节点名不匹配时出现空策略组。

添加支付规则：编辑 `rules/Payment.list`。该文件用于支付和账号稳定，不应放进 Claude 或 AI 规则。使用时应选择与真实账单地址、付款方式和账号地区一致的出口，不用于规避税费或伪造所在地。

iPhone `192.168.5.50` 分流：`rules/PhoneClaude.list` 使用 `SRC-IP-CIDR,192.168.5.50/32`，让该设备公网流量走 `🧠 Claude固定家宽`。需要在路由器 DHCP 中做静态租约；iPhone 可能需要关闭“私有 Wi-Fi 地址”，或在路由器绑定当前私有 MAC。由于 `LocalAreaNetwork.list` 放在 `PhoneClaude.list` 前面，访问 NAS、Mac、路由器等局域网设备仍然直连。

Apple 默认 `DIRECT`，用于减少 App Store、Apple ID、iCloud 登录和设备验证异常。

`🐟 漏网之鱼` 默认 `DIRECT`，用于降低未知国内站点、学校系统、验证码、支付页面误走代理的概率。需要代理的域名应显式加入 `rules/ProxyLite.list` 或对应服务规则。

流媒体和广告规则默认注释。Netflix、TikTok、国外媒体、BanAD、BanProgramAD 等模板保留在配置里，未来需要时再手动取消注释并检查影响。

## 检查

运行：

```bash
python3 scripts/check_rules.py
```

脚本会检查 `.list` 重复规则、异常空行、非法规则类型、URL 误写为 `DOMAIN-SUFFIX`、敏感信息、主配置引用的本地规则文件、PhoneClaude/Claude/AI/Payment 顺序、AI 与 Claude 规则隔离、Payment 独立性、低内存大型 ruleset 是否仍关闭、策略组兜底和广告 ruleset 是否仍处于注释状态。

## 安全原则

不要提交任何真实订阅链接、真实节点信息、proxy-providers URL、token、password、passwd、secret、bearer，或 `ss://`、`ssr://`、`vmess://`、`vless://`、`trojan://`、`hysteria://`、`hy2://` 链接。
