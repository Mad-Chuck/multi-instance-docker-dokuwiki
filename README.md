# multi-instance-docker-dokuwiki
Multi-instance webservice that allows users to create their own instances of DokuWiki. Something like fandom.org on DokuWiki on Docker.

## Directory structure
- /core_engines - folder with dokuwiki core files, plugins and templates. Each directory inside this folder should be listed in dokuwiki versions.

- /wikis_data - folder with user configuration files of their dokuwiki instance.

## Docker commands

start single

```shell script
docker-compose start dokuwiki1
```

lub

```shell script
docker-compose up -d dokuwiki1
```

stop single

```shell script
docker-compose stop dokuwiki1
```

restart single

```shell script
docker-compose restart dokuwiki1
```
