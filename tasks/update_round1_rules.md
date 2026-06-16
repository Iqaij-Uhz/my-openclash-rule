请检查并修改当前 OpenClash/subconverter 规则仓库。当前仓库已经有第一版配置文件，但我上传后一直没有再手动修改。请在现有版本基础上做“小修 + 增量功能”，不要大幅重构。

核心目标：

1. AI / Claude / Codex / GitHub 稳定；
2. Claude 相关服务固定走指定美国家宽节点；
3. Apple / Microsoft / 支付 / 登录尽量稳定；
4. iPhone 192.168.5.50 的公网流量走 Claude 固定家宽节点，但局域网访问不受影响；
5. 不启用广告拦截；
6. 不加入任何真实订阅链接、节点配置、token、password 或 proxy-providers URL。

请严格完成以下任务。

## 一、保护原始文件

1. 不要修改 `qichiyu_original.ini`。
2. 主配置文件是 `openclash_personal.ini`。
3. 保持 OpenClash/subconverter `[custom]` 格式。
4. 保留：

   * `enable_rule_generator=true`
   * `overwrite_original_rules=true`
5. 如果 `openclash_personal.ini` 中已经使用真实 GitHub raw 用户名，例如 `Iqaij-Uhz`，请继续沿用，不要改回 `USERNAME`。
6. 不要添加任何真实机场订阅链接、真实节点、proxy-provider URL、token、password、secret、ss://、vmess://、vless://、trojan:// 等内容。

## 二、修正第一版配置中的 AI / Claude 问题

请修改 `rules/AI.list`：

1. 删除所有 Claude / Anthropic 相关规则。
2. 删除错误规则：

   * `DOMAIN-SUFFIX,claude.ai.com`
3. `rules/AI.list` 只保留非 Claude 的 AI 服务，例如：

   * OpenAI
   * ChatGPT
   * Codex
   * Gemini
   * Perplexity
   * Cursor 相关 AI 服务
   * 其他明确属于 AI 的服务
4. 不要把 Claude / Anthropic 规则放进 `AI.list`。
5. 谨慎处理通用第三方服务：

   * `auth0.com`
   * `stripe.com`
   * `intercom.io`
   * `sentry.io`

   这些不要默认放进 `AI.list`，避免大量无关网站误走 AI 节点。需要时只允许作为注释模板保留，并注明“确认具体服务需要后再启用”。

请修改 `rules/Claude.list`：

1. 保留 Claude / Anthropic / Claude Code 核心规则，例如：

   * `DOMAIN-SUFFIX,claude.ai`
   * `DOMAIN-SUFFIX,anthropic.com`
   * `DOMAIN,api.anthropic.com`
   * `DOMAIN,console.anthropic.com`
   * `DOMAIN,statsig.anthropic.com`
2. `DOMAIN-SUFFIX,sentry.io` 默认注释掉，并注明：

   * 这是通用错误监控服务；
   * 只有确认 Claude Code 运行确实需要时再取消注释。
3. 不要把 Claude 规则重复放回 `AI.list`。
4. `openclash_personal.ini` 中 `Claude.list` 的 ruleset 必须早于 `AI.list`。

## 三、清理重复规则

请去重，但不要大幅重构规则文件。

重点检查：

1. `rules/Direct.list` 中的重复项，例如：

   * `DOMAIN-SUFFIX,hao123.com`
   * `IP-CIDR,219.146.1.66/32,no-resolve`
   * `DOMAIN-SUFFIX,smtcdns.net`

2. `rules/ProxyLite.list` 中的重复项，例如：

   * `DOMAIN-SUFFIX,dns.google`
   * `DOMAIN-SUFFIX,dns.quad9.net`

要求：

1. 只删除重复项。
2. 不要大规模删减 `Direct.list`。
3. 不要改变我现有的整体分流逻辑。

## 四、新增支付服务 Payment.list

请新增：

* `rules/Payment.list`
* `💳 支付服务` 策略组

`rules/Payment.list` 初始内容包含 Stripe 相关域名：

```ini
# Payment services
# Used for payment/account stability. Choose an outlet consistent with the real billing address,
# payment method, and account region. Do not use this to evade tax or misrepresent location.

DOMAIN-SUFFIX,stripe.com
DOMAIN-SUFFIX,stripe.network
DOMAIN,js.stripe.com
DOMAIN,checkout.stripe.com
```

请在 `openclash_personal.ini` 中新增 ruleset：

```ini
ruleset=💳 支付服务,https://raw.githubusercontent.com/Iqaij-Uhz/my-openclash-rule/main/rules/Payment.list
```

如果当前配置仍然使用 `USERNAME` 占位符，则保持同样风格：

```ini
ruleset=💳 支付服务,https://raw.githubusercontent.com/USERNAME/my-openclash-rule/main/rules/Payment.list
```

策略组建议：

```ini
custom_proxy_group=💳 支付服务`select`[]DIRECT`[]🏡 美国家宽备用`[]🇺🇲 美国节点`[]🐸 手动切换
```

要求：

1. 不要把 Stripe 放进 `Claude.list`。
2. 不要把 Stripe 放进 `AI.list`。
3. `💳 支付服务` 不要使用 fallback。
4. `💳 支付服务` 不要使用 load-balance。
5. `💳 支付服务` 不要自动测速切换。
6. 支付服务的目标是支付和账号稳定，应选择与真实账单地址、付款方式和账号地区一致的出口，不用于规避税费或伪造所在地。
7. `Payment.list` 的 ruleset 建议放在 `Claude.list` / `AI.list` 之后，GitHub / Google / Microsoft / Apple 等常用服务之前。

## 五、新增 iPhone 192.168.5.50 公网全局走 Claude 家宽，但局域网直连

请新增：

* `rules/PhoneClaude.list`

内容为：

```ini
# iPhone 192.168.5.50: route all non-LAN traffic to Claude fixed residential node
SRC-IP-CIDR,192.168.5.50/32
```

请修改 `openclash_personal.ini` 的 ruleset 顺序，确保：

1. `LocalAreaNetwork.list` 必须放在最前面，并走 `🎯 全球直连`。
2. `PhoneClaude.list` 必须放在 `LocalAreaNetwork.list` 之后。
3. `PhoneClaude.list` 必须早于：

   * `Direct.list`
   * `ProxyLite.list`
   * `Claude.list`
   * `AI.list`
   * `Payment.list`
   * GitHub
   * Google
   * Microsoft
   * Apple
   * YouTube
   * Telegram
   * China
   * FINAL
4. 这样可以保证：

   * iPhone 访问局域网设备时仍然直连；
   * iPhone 访问公网时走 `🧠 Claude固定家宽`。

修改后的 ruleset 开头顺序应类似：

```ini
; 局域网永远直连，必须放最前，避免 iPhone 访问 NAS / Mac Studio / 路由器也被代理
ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/LocalAreaNetwork.list

; iPhone 192.168.5.50 的非局域网流量走 Claude 固定家宽
ruleset=🧠 Claude固定家宽,https://raw.githubusercontent.com/Iqaij-Uhz/my-openclash-rule/main/rules/PhoneClaude.list

; 自定义直连 / 代理 / Claude / AI / 支付
ruleset=🎯 全球直连,https://raw.githubusercontent.com/Iqaij-Uhz/my-openclash-rule/main/rules/Direct.list
ruleset=🚀 节点选择,https://raw.githubusercontent.com/Iqaij-Uhz/my-openclash-rule/main/rules/ProxyLite.list
ruleset=🧠 Claude固定家宽,https://raw.githubusercontent.com/Iqaij-Uhz/my-openclash-rule/main/rules/Claude.list
ruleset=🤖 AI,https://raw.githubusercontent.com/Iqaij-Uhz/my-openclash-rule/main/rules/AI.list
ruleset=💳 支付服务,https://raw.githubusercontent.com/Iqaij-Uhz/my-openclash-rule/main/rules/Payment.list

; 基础放行
ruleset=🎯 全球直连,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/UnBan.list
```

如果当前配置仍然使用 `USERNAME` 占位符，则保持同样风格，不要强行改成 `Iqaij-Uhz`。

## 六、确认 Claude 固定家宽策略组

请检查 `openclash_personal.ini` 中以下策略组是否存在且正确：

1. `🧠 Claude固定家宽`

   * 第一版只精确匹配：

     ```regex
     ^BGP智能路由-美国07-家宽-ss-x2$
     ```
   * 不要使用 fallback。
   * 不要使用 load-balance。
   * 不要使用 url-test。

2. `🏡 美国家宽备用`

   * 匹配：

     ```regex
     ^BGP智能路由-美国(07|08|09|10)-家宽-ss-x2$
     ```

3. `🐟 漏网之鱼`

   * 默认 `DIRECT`
   * 保留可选项：

     * `DIRECT`
     * `🚀 节点选择`
     * `🐸 手动切换`

4. `🍎 Apple`

   * 默认优先 `DIRECT`
   * 保留可选项：

     * `DIRECT`
     * `🚀 节点选择`
     * `🐸 手动切换`

5. 广告相关策略组可以保留模板：

   * `🛑 广告拦截`
   * `🍃 应用净化`

   但广告相关 ruleset 必须全部注释，不启用。

## 七、规则顺序最终要求

请确保 `openclash_personal.ini` 中 ruleset 总体顺序为：

1. `LocalAreaNetwork.list` → `🎯 全球直连`
2. `PhoneClaude.list` → `🧠 Claude固定家宽`
3. `Direct.list` → `🎯 全球直连`
4. `ProxyLite.list` → `🚀 节点选择`
5. `Claude.list` → `🧠 Claude固定家宽`
6. `AI.list` → `🤖 AI`
7. `Payment.list` → `💳 支付服务`
8. `UnBan.list` → `🎯 全球直连`
9. 广告规则：默认注释，不启用
10. GitHub → `👨🏿‍💻 GitHub`
11. Google → `🍀 Google`
12. Microsoft → `🪟 Microsoft`
13. Apple → `🍎 Apple`
14. YouTube → `📹 YouTube`
15. Telegram → `📲 Telegram`
16. ProxyGFWlist → `🚀 节点选择`
17. GEOSITE,geolocation-!cn → `🚀 节点选择`
18. ChinaDomain → `🎯 全球直连`
19. ChinaCompanyIp → `🎯 全球直连`
20. GEOSITE,CN → `🎯 全球直连`
21. GEOIP,CN,no-resolve → `🎯 全球直连`
22. FINAL → `🐟 漏网之鱼`

关键检查：

1. `Claude.list` 必须早于 `AI.list`。
2. `AI.list` 必须早于 Google、Microsoft、ProxyGFWlist、FINAL。
3. `PhoneClaude.list` 必须早于所有公网规则。
4. `LocalAreaNetwork.list` 必须早于 `PhoneClaude.list`。
5. 广告 ruleset 必须保持注释状态。
6. `FINAL` 必须走 `🐟 漏网之鱼`，而 `🐟 漏网之鱼` 默认 `DIRECT`。

## 八、更新检查脚本 scripts/check_rules.py

请更新或创建 `scripts/check_rules.py`，用于检查：

1. `.list` 文件重复规则。
2. 空行过多。
3. 非法规则类型。
4. 允许以下规则类型：

   * DOMAIN
   * DOMAIN-SUFFIX
   * DOMAIN-KEYWORD
   * IP-CIDR
   * IP-CIDR6
   * GEOIP
   * GEOSITE
   * SRC-IP-CIDR
   * DST-PORT
   * PROCESS-NAME
   * RULE-SET
   * MATCH
   * FINAL
5. 检查是否把 URL 误写成 `DOMAIN-SUFFIX`，例如：

   * `DOMAIN-SUFFIX,https://example.com`
6. 检查敏感信息：

   * 机场订阅链接
   * proxy-provider URL
   * token
   * password
   * passwd
   * secret
   * bearer
   * clash subscription
   * ss://
   * ssr://
   * vmess://
   * vless://
   * trojan://
   * hysteria://
   * hy2://
7. 检查 `rules/PhoneClaude.list` 是否存在。
8. 检查 `rules/Payment.list` 是否存在。
9. 检查 `PhoneClaude.list` 中是否包含：

   * `SRC-IP-CIDR,192.168.5.50/32`
10. 检查 `LocalAreaNetwork.list` 是否在 `PhoneClaude.list` 前面。
11. 检查 `PhoneClaude.list` 是否在 Direct、ProxyLite、Claude、AI、Payment、FINAL 前面。
12. 检查 `Claude.list` 是否在 `AI.list` 之前。
13. 检查 `AI.list` 是否在 Google、Microsoft、ProxyGFWlist、FINAL 之前。
14. 检查广告 ruleset 是否仍处于注释状态。
15. 检查 `AI.list` 中是否仍含 Claude / Anthropic 相关规则，如有则报错。
16. 检查 `Claude.list` 中 `sentry.io` 是否为注释状态，如未注释则给出 warning 或 error。
17. 检查 `Payment.list` 是否没有被放入 `Claude.list` 或 `AI.list`。

## 九、更新 README.md

请更新 `README.md`，补充说明：

1. 仓库用途。
2. `openclash_personal.ini` 是正式使用的主配置。
3. `qichiyu_original.ini` 是原始参考文件，不直接修改。
4. 如何添加直连规则：`rules/Direct.list`。
5. 如何添加代理规则：`rules/ProxyLite.list`。
6. 如何添加普通 AI 规则：`rules/AI.list`。
7. 如何添加 Claude 专用规则：`rules/Claude.list`。
8. Claude 为什么单独走固定美国家宽。
9. 为什么 Claude 固定家宽不使用 fallback、load-balance、url-test。
10. `rules/Payment.list` 的用途：

    * 用于支付和账号稳定；
    * 不应放进 Claude 或 AI；
    * 应选择与真实账单地址、付款方式和账号地区一致的出口；
    * 不用于规避税费或伪造所在地。
11. iPhone 192.168.5.50 分流说明：

    * 需要在路由器 DHCP 中做静态租约；
    * iPhone 可能需要关闭“私有 Wi-Fi 地址”，或在路由器绑定当前私有 MAC；
    * 因为 LocalAreaNetwork.list 放在 PhoneClaude.list 前面，所以访问局域网设备仍然直连；
    * 该 iPhone 的公网流量会走 `🧠 Claude固定家宽`。
12. Apple 默认 DIRECT 的原因：

    * 减少 App Store / Apple ID 登录异常。
13. 漏网之鱼默认 DIRECT 的原因：

    * 提高国内网站和未知流量稳定性。
14. 广告和流媒体规则当前默认注释关闭。
15. 如何运行：

    ```bash
    python3 scripts/check_rules.py
    ```
16. 不要提交真实订阅链接、节点信息、token、password、proxy-providers URL。

## 十、更新 CHANGELOG.md

请更新 `CHANGELOG.md`，记录本次修改：

1. 修正 AI / Claude 规则分离。
2. 注释通用第三方服务，避免误分流。
3. 新增 `rules/Payment.list` 和 `💳 支付服务`。
4. 新增 `rules/PhoneClaude.list`。
5. 调整 ruleset 顺序，使 iPhone 公网走 Claude 家宽但局域网直连。
6. 清理重复规则。
7. 更新检查脚本。
8. 更新 README。

## 十一、完成后请输出总结

完成后请总结：

1. 修改了哪些文件。
2. 新增了哪些文件。
3. 删除或注释了哪些内容。
4. 当前 ruleset 顺序是否符合要求。
5. 当前广告规则是否仍然关闭。
6. `Claude.list` 是否在 `AI.list` 前面。
7. `LocalAreaNetwork.list` 是否在 `PhoneClaude.list` 前面。
8. `PhoneClaude.list` 是否在所有公网规则前面。
9. `Payment.list` 是否独立于 Claude / AI。
10. 我下一步应该人工检查什么。

请最后运行或提示我运行：

```bash
python3 scripts/check_rules.py
```

如果检查脚本报错，请修复后再总结。

