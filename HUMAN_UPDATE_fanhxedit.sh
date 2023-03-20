#!/bin/bash
find . -type f -name "*.fa" -print0 | xargs -0 sed -i '' "s/ENS0/ENSHOM0/g" &&
find . -type f -name "*.fa" -print0 | xargs -0 sed -i '' "s/_M.*//g" &&
find . -type f -name "*.fa" -print0 | xargs -0 sed -i '' "s/MGP_//g" &&
find . -type f -name "*.fa" -print0 | xargs -0 sed -i '' "s/EiJ_//g" &&
find . -type f -name "*.fa" -print0 | xargs -0 sed -i '' "s/_.*//g" &&
find . -type f -name "*.nhx" -print0 | xargs -0 sed -i '' "s/ENS0/ENSHOM0/g" &&
find . -type f -name "*.nhx" -print0 | xargs -0 sed -i '' "s/MGP_//g" &&
find . -type f -name "*.nhx" -print0 | xargs -0 sed -i '' "s/DD=Y:/DD=Y:D=N:/g" &&
find . -type f -name "*.nhx" -print0 | xargs -0 sed -i '' "s/DD=N/DD=N:D=N:/g" &&
find . -type f -name "*.nhx" -print0 | xargs -0 sed -i '' "s/EiJ_//g"
