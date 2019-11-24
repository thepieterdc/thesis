#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "Syntax: ./present.sh folder"
  exit 1
fi

pdfpc "$1/presentation.pdf"
