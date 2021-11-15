## Jit Repo Scan

### To Run:
* Clone repo
* Run `docker-compose up`
* Go to `localhost:5000`


### Requests
* `/`: Welcome
* `/reporisk/repo-src/num-or-repos-to-process`:
    * repo-src = repositories location (currently only github supported)
    * num-or-repos-to-process = amount of trending repos to process (between 1 and 25)