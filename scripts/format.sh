# TODO: replace this script with a pre-commit hook

#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <path>"
  exit 1
fi

TARGET_PATH=$1
black $TARGET_PATH && isort $TARGET_PATH

if [ $? -eq 0 ]; then
  echo "Successfully formatted and sorted imports for $TARGET_PATH"
else
  echo "There was an error formatting or sorting imports for $TARGET_PATH"
fi
