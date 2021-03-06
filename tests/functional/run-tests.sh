#!/usr/bin/env bash
## Run functional tests.

## The input files are tracked by git, so any changes to their original
## content will be shown.

if [[ -n $(git status -s) ]]; then
    printf "Working tree should be clean for tests.\n"
    exit 1
fi

inputdir=test-input
files=($(ls "$inputdir"/file*txt))

function check_gone (){
    for f in ${files[@]}; do
        [ -e $f ] && printf "$f exists but shouldn't\n" 1>&2
    done
}

blind -h > /dev/null || exit 1

blind mask ${files[@]} > /dev/null
printf "\nShould be four letter file names:\n"
ls "$inputdir"/*.txt
check_gone
blind unmask "$inputdir"/blind-map-*.csv
rm "$inputdir"/blind-map-*.csv

blind mask -n ${files[@]} > /dev/null
printf "\nShould be number files names:\n"
ls "$inputdir"/*.txt
check_gone
blind unmask "$inputdir"/blind-map-*.csv
rm "$inputdir"/blind-map-*.csv

printf "\nShould fail with conflict error:\n"
blind mask -n "$inputdir"/0 "$inputdir"/1

if [[ -z $(git status -s) ]]; then
    printf "\nNo file content changed. Check test output.\n"
else
    printf "\nSome tests failed.\n"
    exit 2
fi
