#!/bin/bash

VERSION=$(cat VERSION)

# Restore original placeholder first (optional, only needed if not using template)
sed -i 's/Current Version: `.*`/Current Version: `{{VERSION}}`/' README.md

# Replace placeholder with actual version
sed -i "s/{{VERSION}}/$VERSION/" README.md