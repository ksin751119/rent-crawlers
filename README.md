# rent-crawler

for personal usage.

## required

### packages or libs

* python-dotenv
* selenium
* bs4
* pandas


### chromedriver

[download](https://sites.google.com/chromium.org/driver/downloads)

## how to use

### 591

1. Create `.env` in root folder.
2. Go to [https://rent.591.com.tw/list](https://rent.591.com.tw/list) and filter your conditions.
3. Copy url and paste to `.env` like this:

```
591_FILTER_URL=<Your url>
```

4. Open terminal and enter this command:

```
python3 591/crawler_selenium.py
```

5. Result file will be located at: `temp/591recommend.html` and `temp/591normal.html`
