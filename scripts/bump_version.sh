#!/bin/bash

PART=${1:-patch}  # Accept "major", "minor", or "patch" (default to patch)

read -r MAJOR MINOR PATCH <<<$(cat VERSION | tr '.' ' ')

case $PART in
  major) ((MAJOR+=1)); MINOR=0; PATCH=0 ;;
  minor) ((MINOR+=1)); PATCH=0 ;;
  patch) ((PATCH+=1)) ;;
  *) echo "Invalid part: use major, minor, or patch"; exit 1 ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
echo "$NEW_VERSION" > VERSION

echo "Bumped version to $NEW_VERSION"