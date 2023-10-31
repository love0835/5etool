#!/bin/bash

echo "Delete unnecessary files for hosting 5etools..."

rm *.md *.json *.yml || true
rm -r test/ || true
rm -r node/ || true
rm -r node_modules/ || true
rm .gitignore .eslintrc.js .editorconfig || true
