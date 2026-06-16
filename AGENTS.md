# AGENTS.md

## Project

This repository is a personal OpenClash / subconverter rule project.

## Core goals

- AI services should be stable.
- Research access should be stable.
- GitHub access should be stable.
- Account login should be stable.
- Do not prioritize complex streaming rules or aggressive ad blocking.

## Safety rules

Never add or commit:

- Real proxy subscription URLs
- Real node definitions
- proxy-providers URLs
- tokens
- passwords
- secrets
- ss://, ssr://, vmess://, vless://, trojan://, hysteria://, hy2:// links

## Maintenance rules

- Do not modify qichiyu_original.ini unless explicitly requested.
- Use qichiyu_original.ini only as a reference.
- Keep qichiyu_my.ini compatible with OpenClash / subconverter [custom] format.
- Keep rules simple and maintainable.
- Prefer explicit rule files under rules/.
- Run scripts/check_rules.py after changes when available.
