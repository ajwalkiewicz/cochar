#!/bin/bash
# Cochar - create a random character for Call of Cthulhu RPG 7th ed. 
# Copyright (C) 2023  Adam Walkiewicz

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

SEMVER_REGEX="^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)(\\-[0-9A-Za-z-]+(\\.[0-9A-Za-z-]+)*)?(\\+[0-9A-Za-z-]+(\\.[0-9A-Za-z-]+)*)?$"


function validate_version {
    if $SOFTWARE_VERSION_FLAG; then
        local version=$1
        if [[ "$version" =~ $SEMVER_REGEX ]]; then
            # if a second argument is passed, store the result in var named by $2
            if [ "$#" -eq "2" ]; then
                local major=${BASH_REMATCH[1]}
                local minor=${BASH_REMATCH[2]}
                local patch=${BASH_REMATCH[3]}
                local prere=${BASH_REMATCH[4]}
                local build=${BASH_REMATCH[5]}
                eval "$2=(\"$major\" \"$minor\" \"$patch\" \"$prere\" \"$build\")"
            else
                echo "Version valid"
            fi
        else
            error "version $version does not match the semver scheme 'X.Y.Z(-PRERELEASE)(+BUILD)'. See help for more information."
        fi
    fi
}

change_version(){
    local version=$1
    if $SOFTWARE_VERSION_FLAG; then
        sed -i "s,\"[[:digit:]]\+.[[:digit:]]\+.[[:digit:]]\+.*\",\"$1\",g" setup.py
        sed -i "s,\"[[:digit:]]\+.[[:digit:]]\+.[[:digit:]]\+.*\",\"$1\",g" docs/conf.py
        sed -i "s,\"[[:digit:]]\+.[[:digit:]]\+.[[:digit:]]\+.*\",\"$1\",g" cochar/__init__.py
        echo "Versioin changed to: $1"
    fi
}

main(){
    # install changes locally that to run tests
    pip3 install -e . && \
    # run tests, check packages, uploadd packages
    pytest -q && \
    # change version in all files that contains info about it
    validate_version $SOFTWARE_VERSION && \
    change_version $SOFTWARE_VERSION && \
    # clean dist directory
    rm -rvf -i build && \
    rm -rvf -i $(echo dist/*) && \
    # create package, tar and wheel package
    python3 setup.py sdist bdist_wheel && \
    # check whether packages are good
    twine check $(echo dist/*) && \
    # upload changes to pypi.org 
    twine upload $(echo dist/c*) -u "$USER" -p "$PASS" && \
    # create documentation documentation
    cd docs/ && \
    make html
}

$HELP && echo_help
main
