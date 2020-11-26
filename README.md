# multi-instance-docker-dokuwiki
Multi-instance webservice that allows users to create their own instances of DokuWiki on Docker.

## Table of contents
* [Directory structure](#directory-structure)
* [Setting up](#setting-up)
* [Adding DokuWiki version](#adding-dokuwiki-version)
* [File access and permissions](#file-access-and-permissions)

## Directory structure
    .
    ├── animal.py - CLI to python scripts 
    ├── /cmd_animal - python scripts to manage dokuwiki dockers 
    ├── /core_engines - dir with dokuwiki core files
    │   └── default_version.yml - file with default DokuWiki version for newly added instances
    │
    ├── /wikis_data - dir with dokuwiki instances data 
    ├── docker-compose.yml - config file 
    ├── Dockerfile - docker image 
    └── README.md

## Setting up 

In docker-compose.yml file we should have following traefik configuration:

```yaml
services:
  traefik:
    command:
    - --api.insecure=true
    - --providers.docker=true
    - --providers.docker.exposedbydefault=false
    - --entrypoints.web.address=:80
    container_name: traefik
    image: traefik:v2.3
    ports:
    - 80:80
    - 8080:8080
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
version: '3.3'

```

We then can run the farm with following command:

```shell script
docker-compose up -d
```

To manage dokuwiki dockers use animal.py CLI:
```shell script
python3 animal.py --help
```

Run:
```shell script
python3 animal.py {command} --args
```


It provides several command to manage:

     create
      Create wiki with separated data, running on given engine.
       --name
            service name to create
       --engine=default 
            if arg not given or given engine does not exist - use default version

     ls
      Print all engines and service list.
    
     remove
      Remove service from list if inactive.
       --name
            service name to remove

     restart
      Reboot service
        --name
            service name to restart
     
     run
      Start running service
        --name
            service name
        
     status
      Print status of service
        --name
            service name
        
     stop
      Stop service
        --name
            service name
        
     update
      Update service to newest version
        --name
            service name to update

## Adding DokuWiki version
To add your own DokuWiki version all you need to do is to download DokuWiki form [official download archive](https://download.dokuwiki.org/archive). <br>
Remember to always keep default version directory name in default_version.yml file.
```yaml
version: dokuwiki-2020-07-29
```

When done properly core_engines structure should look like this (2 DokuWiki versions, default version listed in default_version.yml file)
```
/core_engines
├── /dokuwiki-2018-04-22c
│   ├── /bin
│   ├── /conf
│   ├── /data
│   ├── /inc
│   ├── /lib
│   ├── /vendor
│   ├── .htaccess.dist
│   ├── COPYING
│   ├── doku.php
│   ├── feed.php
│   ├── install.php
│   ├── README
│   └── VERSION
│
├── /dokuwiki-2020-07-29
│   ├── /bin
│   ├── /conf
│   ├── /data
│   ├── /inc
│   ├── /lib
│   ├── /vendor
│   ├── .htaccess.dist
│   ├── COPYING
│   ├── doku.php
│   ├── feed.php
│   ├── install.php
│   ├── README
│   └── VERSION
│
└── default_version.yml
```
    

## File access and permissions
DokuWiki's files are in core_engines folder and are mounted "as all" (with default data/conf folders as well).
To disable access to these files (default data/conf, core, plugins, templates etc.) engines volumes are linked in Read Only mode (:ro in the end of arg):
```yaml
volumes:
- ./core_engines/dokuwiki-2020-07-29:/var/www/html:ro
```

We then mount instance's own conf/data folders to rewrite currently mounted default data/conf. To enable access to these folders (data and conf only), we mount them in Read Write mode (:rw in the end of arg):
```yaml
volumes:
- ./wikis_data/test/conf:/var/www/html/conf:rw
- ./wikis_data/test/data:/var/www/html/data:rw
``` 
