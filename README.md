# eBay Scraper
## Overview

This project is a web scraper built with Scrapy to extract data from eBay. It is designed to work with MongoDB to store the scraped data.

## Installation

To install the required dependencies, run:

```bash
pip install -r req.txt
```
## How to Run
### using default 
```bash
scrapy crawl  spider -o mydata.csv
```

### MongoDB Configuration
If you want to enable the MongoDB pipeline, uncomment the following lines in your Scrapy settings (settings.py)
```python
ITEM_PIPELINES = {
    # "ebay_scrapper.pipelines.MongoDBPipeline": 300,
}
```
#### Running with MongoDB

```bash
scrapy crawl -s MONGODB_URI=mongodb://***:****@*****/ -s MONGODB_DATABASE=**** -s MONGODB_COLLECTION=**** spider
```


