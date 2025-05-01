      - name: Bump version
        run: bash scripts/bump_version.sh patch

      - name: Update version in README
        run: bash scripts/update_readme.sh

      - name: Commit and push version bump
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add VERSION README.md
          git commit -m "ci: bump version to $(cat VERSION)" || echo "No changes to commit"
          git push

      - name: Create Git tag
        run: |
          VERSION=$(cat VERSION)
          git tag "v$VERSION"
          git push origin "v$VERSION"
