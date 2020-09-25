## AIS receiver

This project uses the [AIS](https://en.wikipedia.org/wiki/Automatic_identification_system) protocol to store in a database informations of ships around the globe in real-time.

### About this repository

For now, this project allows to fetch ship informations from the [aishub api](aishub.net/api)

In the future, it aims to provide alternative solutions to fetch those from various other providers.

Being able to deal with raw NMEA feeds is one of the major step forward, as it would allow to deal with individual AIS source and most of the major AIS providers.

This repository is meant to be used with the [ais_front](github.com/fractalwire/ais_front) repository as the front-end part. However, it runs independently and has no dependency towards it.

You can run it in a virtual environment. First install dependency:

```
$ pip install -r requirements/dev.txt
```

You'll need a postgres database running somewhere with a database named `ais`.
The following are default values mandatory to connect to the db that can be modified via environment variable if needed:

```
'USER': environ_or_default('POSTGRES_USER', 'postgres'),
'PASSWORD': environ_or_default('POSTGRES_PASSWORD', 'postgres'),
'HOST': environ_or_default('POSTGRES_HOST', '127.0.0.1'),
'PORT': '5432',
```

Then run the services:

```
$ python manage.py waitdb \
 && python manage.py migrate \
 && python manage.py startservices
```