# rent-crawler

for personal usage.

## Notes

* 2024-12-20: 修正爬蟲可能被導向空白頁的問題

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
python3 app/five_nine_one/crawler_selenium.py
```

5. Result file will be located at: `static/591recommend.html` and `static/591normal.html`
