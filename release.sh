git tag -d v1 && git push origin :refs/tags/v1
git tag -a -m "Release v1" v1 && git push --follow-tags
