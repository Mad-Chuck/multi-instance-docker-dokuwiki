# multi-instance-docker-dokuwiki
Multi-instance webservice that allows users to create their own instances of DokuWiki on Docker.

## Directory structure
.<br>
├── animal.py - CLI to python scripts <br>
├── /cmd_animal - python scripts to manage dokuwiki dockers <br>
├── /core_engines - dir with dokuwiki core files<br>
├── /wikis_data - dir with dokuwiki instances data <br>
├── docker-compose.yml - config file <br>
├── Dockerfile - docker image <br>
└── README.md<br>

## Running 

todo: how to start traefik

```shell script
todo...
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
        
     start
      Start service
        --name
        
     status
      Print status of service
        --name
        
     stop
      Stop service
        --name
        
     update
      Update service to newest version
        --name

## Security
To disable access to dokuwiki core files, plugins and templates, 
engines volumes are linked in Read Only mode (:ro in the end of arg):
```
volumes:
- ./core_engines/dokuwiki-2020-07-29:/var/www/html:ro
```

To enable access to dokuwiki data and configuration, data and configuartion dirs 
are linked in Read Write mode (:rw in the end of arg):
```
volumes:
- ./wikis_data/test/conf:/var/www/html/conf:rw
- ./wikis_data/test/data:/var/www/html/data:rw
``` 