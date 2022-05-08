#!/bin/bash
# Update Package Version
# This script upload package to pypi.org.
# Before that it run tests 
#
# Author: Adam Walkiewicz

# VERBOSE=false
HELP=false
SOFTWARE_VERSION_FLAG=false
SOFTWARE_VERSION=""
USER=$(head -n 1 credentials)
PASS=$(tail -n 1 credentials)

while getopts vhs: flag; do
    case "${flag}" in
        # v) VERBOSE=true;;
        h) HELP=true;;
        s) SOFTWARE_VERSION_FLAG=true
           SOFTWARE_VERSION=${OPTARG}
           ;;
        *) HELP=true;;
    esac
done

echo_help() {
    echo "Usage: upload [OPTION]"
    echo "Update version of packages"
    echo "Example: upload -vs \"1.1.1\""
    echo ""
    echo "Output control:"
    # echo " -v 			verbose mode"
    echo " -h 			help" 
    echo " -s 			package version"
    echo ""
    echo "Report bugs to github.com/awalkiewicz/randname"
    echo "Copyright (C) 2021 Adam Walkiewicz.  All rights reserved."
    exit 1
}

# echo_verbose () {
#     $VERBOSE && echo -e "$*";
# }

change_version(){
    if $SOFTWARE_VERSION_FLAG; then
        rx='^[^a-zA-Z]*[0-9]+\.[^a-zA-Z]*[0-9]+\.[^a-zA-Z]*[0-9]+[^a-zA-Z]*$'
        if [[ ! "$SOFTWARE_VERSION" =~ $rx ]]; then
            echo -e "\033[31m\e[1minvalid version format: $SOFTWARE_VERSION\e[0m"
            echo_help
        else
            sed -i "s,\"[[:digit:]]\+.[[:digit:]]\+.[[:digit:]]\+\",\"$SOFTWARE_VERSION\",g" setup.py
            sed -i "s,\"[[:digit:]]\+.[[:digit:]]\+.[[:digit:]]\+\",\"$SOFTWARE_VERSION\",g" docs/conf.py
            sed -i "s,\"[[:digit:]]\+.[[:digit:]]\+.[[:digit:]]\+\",\"$SOFTWARE_VERSION\",g" cochar/__init__.py
        fi
    fi
}

main(){
    # install changes locally that to run tests
    pip3 install -e . && \
    # run tests, check packages, uploadd packages
    python3 -m unittest $(echo tests/test_*) && \
    # change version in all files that contains info about it
    change_version && \
    # clean dist directory
    rm -rv build  && \
    rm -rv -i $(echo dist/*) && \
    # create package, tar and wheel package
    python3 setup.py sdist bdist_wheel && \
    # check whether packages are good
    twine check $(echo dist/*) && \
    # upload changes to pypi.org 
    twine upload $(echo "dist/c*") -u "$USER" -p "$PASS" && \
    # create documentation documentation
    cd docs/ && \
    make html
}

$HELP && echo_help
main
