"""Version policy for the sealed Hyperflow execution contract."""

from __future__ import annotations

from dataclasses import dataclass

CONTRACT_VERSION = "1.0.0"


@dataclass(frozen=True)
class SemVer:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, version: str) -> "SemVer":
        parts = str(version).split('.')
        if len(parts) != 3:
            raise ValueError(f"Invalid contract version {version!r}; expected MAJOR.MINOR.PATCH")
        try:
            major, minor, patch = (int(part) for part in parts)
        except ValueError as exc:
            raise ValueError(f"Invalid contract version {version!r}; expected numeric semver") from exc
        return cls(major=major, minor=minor, patch=patch)


def assert_contract_version(version: str, *, expected: str = CONTRACT_VERSION) -> str:
    parsed = SemVer.parse(version)
    target = SemVer.parse(expected)
    if parsed != target:
        raise ValueError(
            f"Contract version drift detected: got {version!r}, expected {expected!r}. "
            "Bump the contract version deliberately before changing the sealed surface."
        )
    return version


def is_compatible_contract_version(version: str, *, baseline: str = CONTRACT_VERSION) -> bool:
    current = SemVer.parse(version)
    target = SemVer.parse(baseline)
    return current.major == target.major and (current.minor, current.patch) >= (target.minor, target.patch)
