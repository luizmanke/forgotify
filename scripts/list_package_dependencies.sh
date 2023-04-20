#!/bin/bash

_list_package_dependencies_recursively() {
    package_path="$1"

    REMOVE_QUOTES='s#"##g'
    REMOVE_PREVIOUS_DIRS='s#\.\./##g'
    REMOVE_AFTER_COMMA='s#,.*##g'

    relative_dependencies_path=$(grep -o '"\.\./.*"' "$package_path"/pyproject.toml)
    absolute_dependencies_path=$(
        echo "$relative_dependencies_path" | 
        sed -e $REMOVE_QUOTES -e $REMOVE_PREVIOUS_DIRS -e $REMOVE_AFTER_COMMA
    )

    echo "$absolute_dependencies_path"

    if [ -n "$absolute_dependencies_path" ]
    then
        for dependency_path in $absolute_dependencies_path
        do
            echo "$(_list_package_dependencies_recursively $dependency_path)"
        done
    fi
}

main() {
    package_path="$1"

    dependencies_path=$(_list_package_dependencies_recursively "$package_path")

    echo $dependencies_path
}

main $1
