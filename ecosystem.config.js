module.exports = {
  apps: [{
    name: "591-crawler",
    script: "./rent-crawlers/app/five_nine_one/crawler_selenium.py",
    interpreter: "python3",
    cron_restart: "*/30 * * * *",  // 每30分鐘執行一次
    watch: false
  }]
}
