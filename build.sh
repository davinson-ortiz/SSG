#!/bin/bash

if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  # Windows
  python src/main.py "/ssg/"
else
  # Linux/macOS
  python3 src/main.py "/ssg/"
fi