# robots-web-scraper
A web scraper to analyze robots.txt files

## 1. Full Documentation
Refer to the [Wiki](https://github.com/acchiao/robots-web-scraper/wiki) for full documentation, examples, tests, operational details, notes, and other information.

## 2. Quick Start Guide

### Getting the Data

1. `wget http://s3.amazonaws.com/alexa-static/top-1m.csv.zip`
2. `unzip top-1m.csv.zip`

### Installation

1. `git clone https://github.com/acchiao/robots-web-scraper`
2. `cd robots-web-scraper`
3. `virtualenv venv --python=python3` or `python3 -m virtualenv venv`
4. `source venv/bin/activate`
5. `pip install -r requirements.txt`


## References
- [Intoli](https://intoli.com/blog/analyzing-one-million-robots-txt-files/)
