#!/bin/bash

if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  # Windows
  python -m unittest discover -s src
else
  # Linux/macOS
  python3 -m unittest discover -s src
fi
