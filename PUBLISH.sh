#!/bin/sh
set -eu
printf 'Your authorized GitHub OWNER/REPOSITORY: '
read -r repo
printf 'Type PUBLISH to approve public source upload: '
read -r approval
[ "$approval" = PUBLISH ] || exit 0
python3 scripts/publish.py --repo "$repo" --public --approve-publication
