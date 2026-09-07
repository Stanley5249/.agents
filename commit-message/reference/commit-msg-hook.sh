#!/bin/sh
# Install: copy to .git/hooks/commit-msg and chmod +x.
# Rejects a commit whose subject line doesn't match this machine's
# Conventional Commits convention, or that has a stray token before
# the type (e.g. a leaked @mention/co-author tag).

msg_file="$1"
subject="$(head -n1 "$msg_file")"

# skip merge commits and fixup!/squash! commits
case "$subject" in
    "Merge "*|fixup!*|squash!*) exit 0 ;;
esac

pattern='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-zA-Z0-9_.-]+\))?!?: .+'

if ! echo "$subject" | grep -qE "$pattern"; then
    echo "commit-msg: subject line doesn't match Conventional Commits format" >&2
    echo "  expected: type(scope): imperative summary" >&2
    echo "  got:      $subject" >&2
    echo "  types: feat fix docs style refactor perf test build ci chore revert" >&2
    exit 1
fi

exit 0
