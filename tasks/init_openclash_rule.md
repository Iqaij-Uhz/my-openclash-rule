请帮我初始化并整理这个 OpenClash/subconverter 规则仓库。

当前目录是我的个人 OpenClash 规则项目。请基于 `qichiyu_original.ini` 创建一个适合我长期维护的 `qichiyu_my.ini`。

项目目标：
我想基于 qichiyu 的 OpenClash/subconverter 配置，构建自己的 `my-openclash-rule` 项目，用于 OpenClash 订阅转换远程配置。我的核心需求是：AI 稳定、科研检索稳定、GitHub 稳定、账号登录稳定，不追求复杂流媒体和强广告拦截。

请严格完成以下任务。

一、创建和整理主配置文件

1. 创建 `openclash_personal.ini`，基于 `qichiyu_original.ini` 精简而来。
2. 保留 OpenClash/subconverter 可用的 `[custom]` 格式。
3. 不要修改 `qichiyu_original.ini`，它只作为原始参考文件。
4. 不要添加任何真实订阅链接、节点信息、token、password、proxy-providers URL。
5. `enable_rule_generator=true` 和 `overwrite_original_rules=true` 保留。

二、策略组设计

请保留并整理以下核心策略组：

* 🚀 节点选择
* 🧠 Claude固定家宽
* 🤖 AI
* 🤖 AI节点
* 🏡 家宽节点
* 🏡 美国家宽备用
* 🍀 Google
* 👨🏿‍💻 GitHub
* 🪟 Microsoft
* 🍎 Apple
* 📹 YouTube
* 📲 Telegram
* 🎯 全球直连
* 🛑 广告拦截
* 🍃 应用净化
* 🐟 漏网之鱼
* 🐸 手动切换
* 🇭🇰 香港节点
* 🇯🇵 日本节点
* 🇺🇲 美国节点
* 🔯 香港故转
* 🔯 日本故转
* 🔯 美国故转

请删除或不启用以下复杂分组：

* 新加坡节点
* 新加坡故转
* 便宜节点
* 自动选择
* 负载均衡
* 其他地区
* Speedtest
* FCM
* PayPal
* 游戏平台
* 国内媒体
* 国外媒体
* Netflix
* TikTok
* Disney
* Spotify
* Bilibili
* OneDrive 单独组
* Copilot 单独组
* 强隐私防护组

但请在 `qichiyu_my.ini` 中用注释方式保留流媒体模板，例如 Netflix、TikTok、流媒体节点。要求是：默认注释关闭，未来我需要时可以取消注释启用。

三、Claude 固定家宽节点

我希望 Claude 网页、Claude Code、Anthropic API 等相关服务固定走一个美国家宽节点。

请新增：

* `rules/Claude.list`
* `🧠 Claude固定家宽` 策略组
* `🏡 美国家宽备用` 策略组

`🧠 Claude固定家宽` 第一版请只精确匹配这个节点：

```ini
^BGP智能路由-美国07-家宽-ss-x2$
```

`🏡 美国家宽备用` 请匹配这些备用节点：

```ini
^BGP智能路由-美国(07|08|09|10)-家宽-ss-x2$
```

注意：

1. Claude 固定家宽不要使用 fallback。
2. Claude 固定家宽不要使用 load-balance。
3. Claude 固定家宽不要自动测速切换。
4. Claude 规则必须早于普通 AI 规则。
5. Claude 不要被 Google、ProxyGFWlist 或 FINAL 抢走。

四、AI 分流设计

请保留 `rules/AI.list`，并新增 `rules/Claude.list`。

`rules/Claude.list` 应该包含 Claude / Anthropic / Claude Code 相关域名，例如：

* claude.ai
* anthropic.com
* api.anthropic.com
* console.anthropic.com
* statsig.anthropic.com
* sentry.io

`rules/AI.list` 应该覆盖除 Claude 以外的常见 AI 服务，包括但不限于：

* ChatGPT
* OpenAI
* OpenAI API
* Codex
* Gemini
* Perplexity
* Cursor 相关 AI 服务
* 其他常见 AI 服务

请注意：

1. `Claude.list` 的 ruleset 必须放在 `AI.list` 前面。
2. `AI.list` 必须放在 Google、Microsoft、ProxyGFWlist、FINAL 前面。
3. 不要把 Claude 规则重复放进普通 AI 分组，避免优先级混乱。
4. 如果不确定某个域名是否属于 Claude，请优先放入 `Claude.list`；如果属于 OpenAI / ChatGPT / Codex，则放入 `AI.list`。

五、节点筛选正则

请根据以下逻辑设置节点筛选：

1. `🐸 手动切换`：包含所有节点。
2. `🇭🇰 香港节点`：匹配香港、HK、Hong Kong。
3. `🇯🇵 日本节点`：匹配日本、JP、Japan。
4. `🇺🇲 美国节点`：匹配美国、US、United States、USA。
5. `🏡 家宽节点`：匹配家宽、家庭、Residential、residential、Home、home、ISP、原生、住宅。
6. `🤖 AI节点`：匹配 AI、ChatGPT、GPT、OpenAI、Claude、Gemini、Anthropic。
7. `🏡 美国家宽备用`：精确匹配 `BGP智能路由-美国07-家宽-ss-x2` 到 `BGP智能路由-美国10-家宽-ss-x2`。
8. `🧠 Claude固定家宽`：只精确匹配 `BGP智能路由-美国07-家宽-ss-x2`。

请修复原配置中策略组名称前后空格不一致的问题，尤其是“便宜节点”这类问题。最终保留的策略组名称必须前后一致。

六、各服务默认策略建议

请按以下默认逻辑组织策略组：

1. `🚀 节点选择`

   * 可选项包括：`🤖 AI节点`、`🔯 香港故转`、`🔯 日本故转`、`🔯 美国故转`、`🇭🇰 香港节点`、`🇯🇵 日本节点`、`🇺🇲 美国节点`、`🐸 手动切换`、`DIRECT`

2. `🧠 Claude固定家宽`

   * 只包含精确匹配的 `BGP智能路由-美国07-家宽-ss-x2`

3. `🤖 AI`

   * 可选项包括：`🤖 AI节点`、`🏡 家宽节点`、`🏡 美国家宽备用`、`🇺🇲 美国节点`、`🐸 手动切换`、`🚀 节点选择`

4. `🍀 Google`

   * 可选项包括：`🚀 节点选择`、`🇯🇵 日本节点`、`🇭🇰 香港节点`、`🇺🇲 美国节点`、`🐸 手动切换`、`DIRECT`

5. `👨🏿‍💻 GitHub`

   * 可选项包括：`🚀 节点选择`、`🔯 日本故转`、`🔯 香港故转`、`🇯🇵 日本节点`、`🇭🇰 香港节点`、`🇺🇲 美国节点`、`🐸 手动切换`

6. `🪟 Microsoft`

   * 可选项包括：`DIRECT`、`🚀 节点选择`、`🇯🇵 日本节点`、`🇭🇰 香港节点`、`🇺🇲 美国节点`、`🐸 手动切换`

7. `🍎 Apple`

   * 默认优先 `DIRECT`
   * 可选项包括：`DIRECT`、`🚀 节点选择`、`🐸 手动切换`
   * 这样做是为了减少 App Store / Apple ID 登录异常。

8. `📹 YouTube`

   * 可选项包括：`🚀 节点选择`、`🇭🇰 香港节点`、`🇯🇵 日本节点`、`🇺🇲 美国节点`、`🐸 手动切换`

9. `📲 Telegram`

   * 可选项包括：`🚀 节点选择`、`🔯 香港故转`、`🔯 日本故转`、`🇭🇰 香港节点`、`🇯🇵 日本节点`、`🇺🇲 美国节点`、`🐸 手动切换`

10. `🐟 漏网之鱼`

    * 默认 `DIRECT`
    * 可选项包括：`DIRECT`、`🚀 节点选择`、`🐸 手动切换`

七、广告拦截要求

我目前不需要广告拦截。

请保留以下策略组作为模板：

* 🛑 广告拦截
* 🍃 应用净化

但是：

1. 广告相关 ruleset 默认全部注释掉。
2. 不要启用强广告拦截。
3. 不要启用强隐私拦截。
4. 不要启用可能影响 App Store、Microsoft、学校网站、验证码、支付页面的激进规则。
5. 如果保留 BanAD / BanProgramAD，也必须注释，不能默认启用。

八、规则文件和 raw 地址

请把以下文件作为我的自定义规则文件：

* `rules/Direct.list`
* `rules/ProxyLite.list`
* `rules/AI.list`
* `rules/Claude.list`

在 `qichiyu_my.ini` 中引用这些文件，但 GitHub raw 地址先使用占位符：

```text
https://raw.githubusercontent.com/USERNAME/my-openclash-rule/main/rules/Direct.list
https://raw.githubusercontent.com/USERNAME/my-openclash-rule/main/rules/ProxyLite.list
https://raw.githubusercontent.com/USERNAME/my-openclash-rule/main/rules/AI.list
https://raw.githubusercontent.com/USERNAME/my-openclash-rule/main/rules/Claude.list
```

不要把 `USERNAME` 替换成真实用户名。

九、规则顺序

请按以下顺序组织 ruleset：

1. 自定义强制直连：

   * `rules/Direct.list` → `🎯 全球直连`

2. 自定义强制代理：

   * `rules/ProxyLite.list` → `🚀 节点选择`

3. Claude 专用规则：

   * `rules/Claude.list` → `🧠 Claude固定家宽`

4. 普通 AI 规则：

   * `rules/AI.list` → `🤖 AI`

5. 局域网和基础放行：

   * LocalAreaNetwork → `🎯 全球直连`
   * UnBan → `🎯 全球直连`

6. 广告规则：

   * 默认注释，不启用

7. 常用服务：

   * GitHub → `👨🏿‍💻 GitHub`
   * Google → `🍀 Google`
   * Microsoft → `🪟 Microsoft`
   * Apple → `🍎 Apple`
   * YouTube → `📹 YouTube`
   * Telegram → `📲 Telegram`

8. 国外代理：

   * ProxyGFWlist → `🚀 节点选择`
   * GEOSITE,geolocation-!cn → `🚀 节点选择`

9. 国内直连：

   * ChinaDomain → `🎯 全球直连`
   * ChinaCompanyIp → `🎯 全球直连`
   * GEOSITE,CN → `🎯 全球直连`
   * GEOIP,CN,no-resolve → `🎯 全球直连`

10. 最终兜底：

* FINAL → `🐟 漏网之鱼`

十、检查脚本

请创建 `scripts/check_rules.py`，用于检查：

1. `.list` 文件是否有重复规则。
2. 是否有空行过多。
3. 是否有非法规则类型。
4. 是否把 URL 误写成 `DOMAIN-SUFFIX`，例如 `DOMAIN-SUFFIX,https://example.com`。
5. 是否出现敏感信息，例如：

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
6. `openclash_personal.ini` 是否引用了不存在的本地规则文件。
7. `openclash_personal.ini` 中是否仍然存在 `USERNAME` 占位符。注意：初始化阶段允许存在，但脚本可以给出 warning，不要作为 fatal error。
8. `Claude.list` 是否在 `AI.list` 之前被引用。
9. `AI.list` 是否在 Google、Microsoft、ProxyGFWlist、FINAL 之前被引用。
10. 广告 ruleset 是否仍处于注释状态。

十一、README 和 CHANGELOG

请更新 `README.md`，说明：

1. 仓库用途。
2. 仓库结构。
3. OpenClash 如何使用 `openclash_personal.ini` 的 raw 地址。
4. 如何添加直连规则。
5. 如何添加代理规则。
6. 如何添加 AI 规则。
7. 如何添加 Claude 专用规则。
8. Claude 为什么单独走固定美国家宽。
9. Apple 为什么默认 DIRECT。
10. 为什么漏网之鱼默认 DIRECT。
11. 如何运行 `scripts/check_rules.py`。
12. 不要提交真实订阅链接、节点信息、token、password、proxy-providers URL。
13. 流媒体和广告规则默认注释，未来需要时再启用。

请更新 `CHANGELOG.md`，记录本次初始化内容。

十二、最终输出要求

完成后请总结：

1. 修改了哪些文件。
2. 新增了哪些文件。
3. 删除或注释了哪些 qichiyu 原始功能。
4. 当前策略组保留情况。
5. 我下一步应该检查什么。

注意：
所有修改以最小可维护为原则，不要堆砌规则，不要改变 Clash/subconverter 基本语法。不要加入任何真实订阅链接、真实节点配置、token、password 或 proxy-providers URL。

