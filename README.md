### opsdroid / skill-docker-daemon


#### Install:
##### **Using this skill directly:**
```
$ git clone https://github.com/codexlynx/opsdroid-skill-docker-daemon.git
$ cd opsdroid-skill-docker-daemon
$ vim configuration.sample.yaml # Add your connector configuration and save as `configuration.yaml`
$ docker-compose up
```

##### **Install this skill in your current opsdroid instance:**
For more information visit: https://docs.opsdroid.dev/en/stable/configuration-reference/#skills

```
skills:
  - name: docker-daemon
    repo: https://github.com/codexlynx/opsdroid-skill-docker-daemon.git
    daemon-url: unix://var/run/docker.sock
    containers-blacklist:
      - opsdroid-skill-docker-daemon_opsdroid_1
```
