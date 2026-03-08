"""
Generate the first version of synthetic work-intake data.
"""
from __future__ import annotations

import random
from typing import Dict, List

import pandas as pd

from src.utils.paths import SYNTHETIC_DATA_DIR, ensure_project_dirs


ROUTING_PATTERNS = {
    "access": [
        "cannot log into account",
        "password reset needed",
        "user locked out",
        "need access to shared folder",
        "authentication not working",
        "permission issue on team site",
        "account access request",
        "mfa challenge failed",
    ],
    "hardware": [
        "laptop battery not charging",
        "monitor not detected",
        "keyboard not working properly",
        "docking station issue",
        "device overheating",
        "headset not connecting",
        "screen flickering intermittently",
        "mouse input lag reported",
    ],
    "software": [
        "application crashes on launch",
        "license activation failed",
        "unable to install tool",
        "error after recent update",
        "software running slowly",
        "tool freezes during use",
        "issue opening desktop app",
        "unexpected pop-up error message",
    ],
    "data_request": [
        "need monthly sales extract",
        "request dashboard export",
        "need access to historical metrics",
        "data pull for audit support",
        "request customer activity report",
        "need csv for weekly review",
        "request usage numbers for presentation",
        "please share latest summary data",
    ],
    "security": [
        "suspicious email reported",
        "possible phishing link clicked",
        "unusual login attempt detected",
        "security review needed",
        "malware alert on workstation",
        "account may be compromised",
        "unexpected security warning appeared",
        "user reported suspicious attachment",
    ],
    "network": [
        "vpn connection keeps dropping",
        "wifi unavailable in office",
        "network latency issue",
        "cannot connect to shared drive",
        "internet outage reported",
        "connection unstable since morning",
        "remote access issue",
        "intermittent connectivity problem",
    ],
}

CHANNELS = ["email", "portal", "chat"]
PRIORITIES = ["low", "medium", "high"]
REQUESTER_TYPES = ["internal", "external", "vip"]

COMMON_PREFIXES = [
    "",
    "user reported ",
    "please assist with ",
    "need help with ",
    "following up on ",
    "request regarding ",
    "urgent: ",
    "issue with ",
]

COMMON_SUFFIXES = [
    "",
    " since this morning",
    " affecting one user",
    " affecting multiple users",
    " after recent changes",
    " and needs follow-up",
    " please investigate",
    " not sure if related to update",
]

TITLE_PREFIXES = [
    "",
    "need help - ",
    "follow-up - ",
    "urgent - ",
    "request - ",
    "issue - ",
]

NOISE_PHRASES = [
    "",
    " user unable to continue work",
    " team asking for update",
    " manager requested quick response",
    " this has happened before",
    " impact appears moderate",
    " impact appears high",
    " workaround not available",
]

QUEUE_HINT_WORDS = {
    "access": ["login", "access", "permission", "account", "mfa"],
    "hardware": ["laptop", "monitor", "keyboard", "dock", "device"],
    "software": ["app", "application", "tool", "install", "license"],
    "data_request": ["report", "export", "metrics", "extract", "data"],
    "security": ["phishing", "security", "malware", "warning", "suspicious"],
    "network": ["vpn", "wifi", "network", "connection", "internet"],
}


def lightly_rephrase(base_text: str) -> str:
    """
    Create a slightly more variable sentence from a base issue description.
    """
    prefix = random.choice(COMMON_PREFIXES)
    suffix = random.choice(COMMON_SUFFIXES)
    noise = random.choice(NOISE_PHRASES)
    return f"{prefix}{base_text}{suffix}{noise}".strip()


def pick_description(queue: str) -> str:
    base = random.choice(ROUTING_PATTERNS[queue])

    # occasionally inject a cross-class shared word without changing the label
    shared_words = ["issue", "request", "problem", "help needed", "unable to proceed"]
    if random.random() < 0.35:
        base = f"{base} - {random.choice(shared_words)}"

    return lightly_rephrase(base)


def generate_title(description: str, queue: str) -> str:
    """
    Generate a short title WITHOUT directly including the queue label name.
    """
    title_prefix = random.choice(TITLE_PREFIXES)

    # Sometimes shorten the title heavily, sometimes keep a richer snippet
    if random.random() < 0.5:
        hint = random.choice(QUEUE_HINT_WORDS[queue])
        title_body = f"{hint} issue"
    else:
        title_body = description[:45].strip(" -")

    return f"{title_prefix}{title_body}".strip()


def generate_sla_risk(
    queue: str,
    priority: str,
    channel: str,
    requester_type: str,
    created_hour: int,
) -> int:
    score = 0

    if priority == "high":
        score += 2
    elif priority == "medium":
        score += 1

    if requester_type == "vip":
        score += 1

    if channel == "email":
        score += 1

    if queue in {"security", "network"}:
        score += 1

    if created_hour < 8 or created_hour > 18:
        score += 1

    # add a small randomness so the rule is not perfectly deterministic
    if random.random() < 0.10:
        score += 1
    if random.random() < 0.08:
        score -= 1

    return 1 if score >= 4 else 0


def generate_record(ticket_num: int) -> Dict:
    queue = random.choice(list(ROUTING_PATTERNS.keys()))
    description = pick_description(queue)
    title = generate_title(description=description, queue=queue)

    channel = random.choice(CHANNELS)
    priority = random.choices(PRIORITIES, weights=[0.25, 0.5, 0.25], k=1)[0]
    requester_type = random.choices(
        REQUESTER_TYPES, weights=[0.65, 0.25, 0.10], k=1
    )[0]
    created_hour = random.randint(0, 23)

    sla_risk = generate_sla_risk(
        queue=queue,
        priority=priority,
        channel=channel,
        requester_type=requester_type,
        created_hour=created_hour,
    )

    return {
        "ticket_id": f"TKT-{ticket_num:05d}",
        "title": title,
        "description": description,
        "channel": channel,
        "priority": priority,
        "requester_type": requester_type,
        "created_hour": created_hour,
        "routing_queue": queue,
        "sla_risk": sla_risk,
    }


def generate_dataset(n_rows: int = 500, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    records: List[Dict] = [generate_record(i) for i in range(1, n_rows + 1)]
    return pd.DataFrame(records)


def main() -> None:
    ensure_project_dirs()

    df = generate_dataset(n_rows=500, seed=42)
    output_path = SYNTHETIC_DATA_DIR / "work_intake_synthetic_v1.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved synthetic dataset to: {output_path}")
    print(f"Shape: {df.shape}")
    print(df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()