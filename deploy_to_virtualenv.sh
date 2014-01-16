#!/usr/bin/env bash
find . -name "*.pyc" -exec rm -rf {} \; && {
    echo "All *.pyc files were deleted"
    fab pack && {
        echo "Successfully build a flaskrilio package"
        pip install -e . && {
            echo "Successfully installed flaskrilio package to virtualenv"
        }
    }
}
