#!/usr/bin/env bash
# Turn this teacher repository (the working solution) into the student
# handout, in place: apply the student/ overlay, drop the teacher-only paths
# of .studentignore, squash history into one commit.
#
# Run it on a copy (a fork or an import into the class organization), never
# on the canonical teacher repository: it rewrites history.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

CANONICAL="heig-tin-info/exercise-armstrong"
origin=$(git remote get-url origin 2>/dev/null || echo "")
if [[ "$origin" == *"$CANONICAL"* && "${STUDENTIZE_FORCE:-}" != "1" ]]; then
  echo "Refusing to studentize the canonical teacher repository ($CANONICAL)." >&2
  exit 1
fi

echo "Applying the student overlay..."
cp -rv student/. .

echo "Removing teacher-only paths..."
grep -v '^\s*\(#\|$\)' .studentignore | xargs rm -rf
rm -f .studentignore

echo "Squashing history into one commit..."
branch=$(git symbolic-ref --short HEAD)
git checkout -q --orphan handout
git read-tree --empty
git ls-files -z --others --exclude-standard | xargs -0 git add --
git commit -q -m "Initial commit"
git branch -M "$branch"

echo "Done. Review the tree, then: git push --force origin HEAD"
