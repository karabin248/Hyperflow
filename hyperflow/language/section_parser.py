import re


SECTION_LABELS = {
    "task": ("Task", "Zadanie"),
    "goal": ("Goal", "Cel"),
    "format": ("Format",),
}


def _build_section_pattern(label_key: str) -> str:
    current_labels = SECTION_LABELS[label_key]
    other_labels = [
        label
        for key, labels in SECTION_LABELS.items()
        if key != label_key
        for label in labels
    ]

    current = "|".join(re.escape(label) for label in current_labels)
    lookahead = "|".join(re.escape(label) for label in other_labels)
    return rf"(?:^|\b)(?:{current}):\s*(.*?)(?=\b(?:{lookahead}):|$)"


SECTION_PATTERNS = {key: _build_section_pattern(key) for key in SECTION_LABELS}


def _clean_value(value: str) -> str:
    return " ".join(value.strip().split())


def parse_sections(text: str) -> dict:
    result = {
        "task": "",
        "goal": "",
        "format": "",
        "body": " ".join(text.strip().split()),
    }

    if not text.strip():
        return result

    for key, pattern in SECTION_PATTERNS.items():
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            result[key] = _clean_value(match.group(1))

    if result["task"] or result["goal"] or result["format"]:
        chunks = []
        for key in ("task", "goal", "format"):
            if result[key]:
                chunks.append(result[key])
        result["body"] = " | ".join(chunks)

    return result