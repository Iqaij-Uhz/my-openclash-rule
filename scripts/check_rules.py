#!/usr/bin/env python3
"""Check local OpenClash/subconverter rule files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "openclash_personal.ini"
RULES_DIR = ROOT / "rules"

VALID_RULE_TYPES = {
    "DOMAIN",
    "DOMAIN-SUFFIX",
    "DOMAIN-KEYWORD",
    "IP-CIDR",
    "IP-CIDR6",
    "GEOIP",
    "GEOSITE",
    "SRC-IP-CIDR",
    "DST-PORT",
    "PROCESS-NAME",
    "RULE-SET",
    "MATCH",
    "FINAL",
}

SENSITIVE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"proxy-provider",
        r"proxy_providers",
        r"\btoken\b",
        r"\bpassword\b",
        r"\bpasswd\b",
        r"\bsecret\b",
        r"\bbearer\b",
        r"clash subscription",
        r"机场订阅",
        r"subscription",
        r"ss://",
        r"ssr://",
        r"vmess://",
        r"vless://",
        r"trojan://",
        r"hysteria://",
        r"hy2://",
    )
]


def is_comment_or_blank(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith("#") or stripped.startswith(";")


def report(kind: str, path: Path, line_no: int | None, message: str) -> str:
    rel = path.relative_to(ROOT)
    location = f"{rel}:{line_no}" if line_no else str(rel)
    return f"{kind}: {location}: {message}"


def check_rule_file(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    seen: dict[str, int] = {}
    blank_run = 0

    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()

        if not line:
            blank_run += 1
            if blank_run > 2:
                warnings.append(report("WARN", path, line_no, "more than two consecutive blank lines"))
            continue

        blank_run = 0

        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(line):
                errors.append(report("ERROR", path, line_no, "possible sensitive information"))

        if line.startswith("#") or line.startswith(";"):
            continue

        if line in seen:
            errors.append(report("ERROR", path, line_no, f"duplicate rule, first seen on line {seen[line]}"))
        else:
            seen[line] = line_no

        rule_type = line.split(",", 1)[0].strip()
        if rule_type not in VALID_RULE_TYPES:
            errors.append(report("ERROR", path, line_no, f"unsupported rule type {rule_type!r}"))

        if line.startswith("DOMAIN-SUFFIX,") and re.search(r",https?://", line, re.IGNORECASE):
            errors.append(report("ERROR", path, line_no, "URL written as DOMAIN-SUFFIX"))

    return errors, warnings


def active_rule_lines(path: Path) -> list[tuple[int, str]]:
    if not path.exists():
        return []
    result: list[tuple[int, str]] = []
    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if line and not line.startswith("#") and not line.startswith(";"):
            result.append((line_no, line))
    return result


def active_rulesets(lines: list[str]) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("ruleset="):
            result.append((line_no, stripped))
    return result


def active_proxy_groups(lines: list[str]) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("custom_proxy_group="):
            result.append((line_no, stripped))
    return result


def find_ruleset_index(rulesets: list[tuple[int, str]], needle: str) -> int | None:
    for index, (_, line) in enumerate(rulesets):
        if needle in line:
            return index
    return None


def require_order(
    errors: list[str],
    rulesets: list[tuple[int, str]],
    before: str,
    after: str,
    message: str,
) -> None:
    before_idx = find_ruleset_index(rulesets, before)
    after_idx = find_ruleset_index(rulesets, after)
    if before_idx is None:
        errors.append(report("ERROR", CONFIG, None, f"{before} is not referenced"))
        return
    if after_idx is None:
        errors.append(report("ERROR", CONFIG, None, f"{after} is not referenced"))
        return
    if before_idx > after_idx:
        errors.append(report("ERROR", CONFIG, None, message))


def check_config() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not CONFIG.exists():
        return [report("ERROR", CONFIG, None, "config file does not exist")], warnings

    text = CONFIG.read_text(encoding="utf-8")
    lines = text.splitlines()

    for line_no, line in enumerate(lines, start=1):
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(line):
                errors.append(report("ERROR", CONFIG, line_no, "possible sensitive information"))

    if "USERNAME" in text:
        warnings.append(report("WARN", CONFIG, None, "USERNAME placeholder still exists"))

    for line_no, line in active_rulesets(lines):
        if "/my-openclash-rule/main/rules/" not in line:
            continue
        local_name = line.rsplit("/rules/", 1)[1].split(",", 1)[0].strip()
        local_path = RULES_DIR / local_name
        if not local_path.exists():
            errors.append(report("ERROR", CONFIG, line_no, f"referenced local rule file {local_name!r} does not exist"))

    rulesets = active_rulesets(lines)
    claude_idx = find_ruleset_index(rulesets, "rules/Claude.list")
    ai_idx = find_ruleset_index(rulesets, "rules/AI.list")
    phone_idx = find_ruleset_index(rulesets, "rules/PhoneClaude.list")

    if claude_idx is None:
        errors.append(report("ERROR", CONFIG, None, "Claude.list is not referenced"))
    if ai_idx is None:
        errors.append(report("ERROR", CONFIG, None, "AI.list is not referenced"))
    if claude_idx is not None and ai_idx is not None and claude_idx > ai_idx:
        errors.append(report("ERROR", CONFIG, None, "Claude.list must be referenced before AI.list"))

    if ai_idx is not None:
        for label in ("GitHub", "Google", "Microsoft", "Apple", "YouTube", "Telegram", "ProxyGFWlist", "FINAL"):
            idx = find_ruleset_index(rulesets, label)
            if idx is not None and ai_idx > idx:
                errors.append(report("ERROR", CONFIG, None, f"AI.list must be referenced before {label}"))

    require_order(errors, rulesets, "LocalAreaNetwork.list", "rules/PhoneClaude.list", "LocalAreaNetwork.list must be before PhoneClaude.list")
    for later in ("rules/Direct.list", "rules/ProxyLite.list", "rules/Claude.list", "rules/AI.list", "rules/Payment.list", "FINAL"):
        require_order(errors, rulesets, "rules/PhoneClaude.list", later, f"PhoneClaude.list must be before {later}")

    for line_no, line in active_rulesets(lines):
        if any(name in line for name in ("BanAD", "BanProgramAD", "BanEasyList", "BanEasyPrivacy", "AdBlock")):
            errors.append(report("ERROR", CONFIG, line_no, "ad ruleset is active; keep it commented by default"))

        if any(name in line for name in ("[]GEOSITE,geolocation-!cn", "[]GEOSITE,CN", "ChinaDomain.list", "ChinaCompanyIp.list")):
            errors.append(report("ERROR", CONFIG, line_no, "large ruleset is active; keep it commented in low-memory mode"))

    explicit_fallbacks = ("[]🐸 手动切换", "[]DIRECT", "[]🚀 节点选择", "[]🏡 美国家宽备用")
    for line_no, line in active_proxy_groups(lines):
        parts = line.split("`")
        if len(parts) < 3 or parts[1] != "select":
            continue
        selector = parts[2]
        has_explicit_fallback = any(fallback in line for fallback in explicit_fallbacks)
        is_all_nodes_group = selector == ".*"
        if not has_explicit_fallback and not is_all_nodes_group:
            errors.append(report("ERROR", CONFIG, line_no, "select proxy group should include an explicit fallback"))

    return errors, warnings


def check_round1_files() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    phone = RULES_DIR / "PhoneClaude.list"
    payment = RULES_DIR / "Payment.list"
    ai = RULES_DIR / "AI.list"
    claude = RULES_DIR / "Claude.list"

    for path in (phone, payment):
        if not path.exists():
            errors.append(report("ERROR", path, None, "required rule file does not exist"))

    phone_rules = [line for _, line in active_rule_lines(phone)]
    if phone.exists() and "SRC-IP-CIDR,192.168.5.50/32" not in phone_rules:
        errors.append(report("ERROR", phone, None, "missing SRC-IP-CIDR,192.168.5.50/32"))

    for line_no, line in active_rule_lines(ai):
        if re.search(r"claude|anthropic", line, re.IGNORECASE):
            errors.append(report("ERROR", ai, line_no, "Claude/Anthropic rule must not be in AI.list"))
        if re.search(r"stripe", line, re.IGNORECASE):
            errors.append(report("ERROR", ai, line_no, "payment rule must not be in AI.list"))

    for line_no, line in active_rule_lines(claude):
        if re.search(r"sentry\.io", line, re.IGNORECASE):
            errors.append(report("ERROR", claude, line_no, "sentry.io must remain commented unless explicitly needed"))
        if re.search(r"stripe", line, re.IGNORECASE):
            errors.append(report("ERROR", claude, line_no, "payment rule must not be in Claude.list"))

    payment_rules = [line for _, line in active_rule_lines(payment)]
    for expected in (
        "DOMAIN-SUFFIX,stripe.com",
        "DOMAIN-SUFFIX,stripe.network",
        "DOMAIN,js.stripe.com",
        "DOMAIN,checkout.stripe.com",
    ):
        if payment.exists() and expected not in payment_rules:
            errors.append(report("ERROR", payment, None, f"missing {expected}"))

    return errors, warnings


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for path in sorted(RULES_DIR.glob("*.list")):
        file_errors, file_warnings = check_rule_file(path)
        errors.extend(file_errors)
        warnings.extend(file_warnings)

    config_errors, config_warnings = check_config()
    errors.extend(config_errors)
    warnings.extend(config_warnings)

    round1_errors, round1_warnings = check_round1_files()
    errors.extend(round1_errors)
    warnings.extend(round1_warnings)

    for warning in warnings:
        print(warning)
    for error in errors:
        print(error)

    if errors:
        print(f"check_rules.py failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"check_rules.py passed: 0 error(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
