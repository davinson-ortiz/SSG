#!/bin/bash

if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  # Windows
  python src/main.py
else
  # Linux/macOS
  python3 src/main.py
fi


if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  # Windows
  cd docs && python -m http.server 8888
else
  # Linux/macOS
  cd docs && python3 -m http.server 8888
fi

