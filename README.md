# Visualizing FRA 2012 LGBT Survey

This app is a small dashboard to help visualize [EU FRA's 2012 survey](https://www.kaggle.com/ruslankl/european-union-lgbt-survey-2012)
about LGBT people's daily lives and rights in the European Union.
It runs as a WSGI application, the prefered serving method is using
[`uvicorn`](https://github.com/encode/uvicorn). Internally, the graphing is done with [`plotly`](https://github.com/plotly/plotly.py)
and front-end is mannaged by [`dash`](https://github.com/plotly/dash).

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
# or
uvicorn visu:server --interface=wsgi --proxy-headers --port 6969 --forwarded-allow-ips='*' --timeout-keep-alive 300
```
## Usage

The app is accessible at [https://alonely.place/vfl](https://alonely.place/vfl) for a live demo.
It is composed of two panes at the time :
  - Overview if the population
  - Poll questions explorer.

They are both pretty self-explanatory : don't hesitate to check it out yourself and play with it a litte.
