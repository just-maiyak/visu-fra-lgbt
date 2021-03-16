# Visualizing FRA 2012 LGBT Survey

This app is a small dashboard to help visualize [EU FRA's 2012 survey]()
about LGBT people's daily lives and rights in the European Union.
It runs as a WSGI application, the prefered serving method is using
[`uvicorn`](). Internally, the graphing is done with [`plotly`]()
and front-end is mannaged by [`dash`]().

## Installation
1. Clone repo
```bash
git pull <url>
```
2. Install requirements in virtual environment
```bash
virtualenv venv
./venv/bin/activatie
pip install -r requirements.txt
```
3. Run server
```bash
uvicorn --interface wsgi visu:server
```
## Usage
