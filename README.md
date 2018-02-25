# inmuebles-24-crawler
A Python project created on February 25, 2018, 08:40 am.

###Prerequisites
You need to install the software and how to install them
```
- python >= 2.7
- pip or conda

```

### Install Scrapy
with pip
```
pip install Scrapy
```
with conda
``` 
conda install -c conda-forge scrapy
```

###Run Script
with default page number
```
scrapy crawl sale_cdmx
```

with custom page number
```
scrapy crawl sale_cdmx -s PAGE_NUMBER=3
```