#!/bin/bash

main() {
    paths=$@

    if [ -n "$paths" ]
    then
        paths_joined=$(printf "%s/**," ${paths[@]})
        paths_joined_trimmed=${paths_joined::-1}

        echo "$paths_joined_trimmed"
    fi
}

main $@
