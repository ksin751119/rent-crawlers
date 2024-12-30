module.exports = {
  apps: [{
    name: "591-crawler",
    script: "./rent-crawlers/app/five_nine_one/crawler_selenium.py",
    interpreter: "python3",
    cron_restart: "*/30 * * * *",
    watch: false,
    autorestart: false,
    log_date_format: "YYYY-MM-DD HH:mm:ss",
    error_file: "logs/591-crawler-error.log",
    out_file: "logs/591-crawler-out.log"
  }]
}
