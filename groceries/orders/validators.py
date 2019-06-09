import re

from django.core.exceptions import ValidationError

SHARE_REGEX = r"^((?P<share>[0-9]{0,2})(?P<initial>[a-z]))*$"
EXTRACT_SHARE_REGEX = r"(?P<share>[0-9]{0,2})(?P<initial>[a-z])"


def validate_shares(value):
    if re.fullmatch(SHARE_REGEX, value) is None:
        raise ValidationError("Value doesn't match the regex")


def parse_shares(value):
    return {
        p.group("initial"): int(p.group("share")) if p.group("share") else 1
        for p in re.finditer(EXTRACT_SHARE_REGEX, value)
    }
