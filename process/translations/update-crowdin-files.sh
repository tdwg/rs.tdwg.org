#!/bin/bash
#

set -e
set -u
shopt -s globstar

branch=translations

# Expects to run on the $branch branch.
if [[ $(git branch --show-current) != "$branch" ]]; then
    echo >&2 "Expected to run only on the $branch branch, to avoid polluting"
    echo >&2 "the repository with intermediate files."
    exit 1
fi

echo "Fetching:"
git fetch --all
echo
echo "Merging any new translations"
git merge origin/crowdin_$branch
echo
echo "Merging any updated sources"
git merge origin/master
echo
echo "Update local master branch to latest origin/master"
git pull origin master:master
echo

# Run the script to update *.??.csv (the source files for Crowdin)
# and *-translations.csv (the resulting files with translations).
echo "Running build-translations.py"
python3 process/translations/build-translations.py
echo
git status
echo

echo "Commit any changes in *.en.csv files on this ($branch) branch."
git add **/*.en.csv
if $(git diff --cached --exit-code --quiet); then
    echo "No changes to *.en.csv files"
else
    git commit --message "Update translation source files for Crowdin."
fi
git push origin crowdin
echo

echo "Commit any new translations to the master branch."
# Move to the master branch without changing the working tree
git symbolic-ref HEAD refs/heads/master && git reset
git add **/*-translations.csv
if $(git diff --cached --exit-code --quiet); then
    echo "No changes to *-translations.csv files"
else
    git commit --message "Updated translations via Crowdin: https://crowdin.com/project/darwin-core"
fi
git push origin master
