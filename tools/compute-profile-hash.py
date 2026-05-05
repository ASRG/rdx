#!/usr/bin/env python3
"""
Compute or verify the integrity hash for an RDX profile JSON file.

Usage:
    python3 tools/compute-profile-hash.py spec/profiles/my-profile.json
    python3 tools/compute-profile-hash.py --verify spec/profiles/my-profile.json

The integrity hash is SHA-256 of the canonical JSON serialization of the profile
with the 'integrity' field replaced by an empty object {}.
Canonical form: keys sorted lexicographically, no extra whitespace, UTF-8 encoded.
"""

import json
import hashlib
import sys
import copy


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def compute_integrity(profile):
    profile_copy = copy.deepcopy(profile)
    profile_copy['integrity'] = {}
    return hashlib.sha256(canonical_json(profile_copy).encode('utf-8')).hexdigest()


def main():
    verify = '--verify' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print("Usage: compute-profile-hash.py [--verify] <profile.json>")
        sys.exit(1)

    with open(args[0]) as f:
        profile = json.load(f)

    computed = compute_integrity(profile)

    if verify:
        stored = profile.get('integrity', {}).get('content', '')
        if computed == stored:
            print(f"OK: integrity hash verified ({computed[:16]}...)")
        else:
            print(f"FAIL: hash mismatch")
            print(f"  stored:   {stored}")
            print(f"  computed: {computed}")
            sys.exit(1)
    else:
        print(computed)


if __name__ == '__main__':
    main()
