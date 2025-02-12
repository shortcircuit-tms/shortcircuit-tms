# How to discard local changes and get the head of the main branch

1. Commit all your changes locally or undo them

2. Follow these steps
```console
git reset --hard HEAD
git clean -fd
git fetch origin
git reset --hard origin/main
git pull
```
