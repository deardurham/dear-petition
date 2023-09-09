# Bookmarklet local dev

Inspiration: 
* https://codesandbox.io/s/zlgp3?file=/src/App.js
* https://support.start.me/hc/en-us/articles/200964881-Install-and-use-our-bookmarklet
* https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## Run tests

```shell
pytest -x dear_petition/portal/tests
```

## Run Django with listen on all interfaces

I'm running this locally (outside of Docker):

```shell
python manage.py runserver 0.0.0.0:8000
```

## Start ngrok

```shell
ngrok http 8000
```

## Compress bookmarklet JS

Copy your ngrok addess to `src/bookmarklet/bookmarklet.js`, then run:

```shell
./node_modules/terser/bin/terser --compress --mangle --output src/bookmarklet/bookmarklet.min.js src/bookmarklet/bookmarklet.js
```

## Copy to React

Copy to `bookmarkletJS` variable in `PageBase.jsx`.

## Add bookmarklet to your bookmarks bar

Log in and drag the "Portal Importer (beta)" button to your bookmarks bar.

## Search and import from eCourts Portal

Visit https://portal-nc.tylertech.cloud/Portal/Home/Dashboard/29 and search for
a record. Click bookmark when on record detail page.

Watch output from Django server.
