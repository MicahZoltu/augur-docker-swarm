# Usage

```
docker-compose up --build --force-recreate --abort-on-container-exit --remove-orphans
```

This will start an ethereum node (Parity) with the Augur contracts setup on it in one container and the Augur UI in another container setup to point at the Parity node.  The Parity UI will be available at `http://localhost:47621` and the Augur UI will be available at `http://localhost:47620`.  You can also send JSON-RPC requests to `http://localhost:47622`.

If you want to run Augur or one of its dependencies against a specific branch/commit, you can edit the docker-compose.yml file `services > augur-ui > build > args > *_commit` to be either a branch name or a commit sha.  These are used to decide what to pull from GitHub when building.
