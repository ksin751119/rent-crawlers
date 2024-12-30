#!/bin/bash

# 設定顏色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 顯示使用方法
show_usage() {
    echo -e "${YELLOW}使用方法:${NC}"
    echo "  ./scripts/pm2.sh [command]"
    echo ""
    echo -e "${YELLOW}可用指令:${NC}"
    echo "  start   - 啟動 PM2 服務"
    echo "  stop    - 停止 PM2 服務"
    echo "  restart - 重啟 PM2 服務"
    echo "  delete  - 刪除 PM2 服務"
    echo "  logs    - 查看日誌"
    echo "  status  - 查看狀態"
    echo "  help    - 顯示此幫助訊息"
}

# 檢查命令是否存在
if ! command -v pm2 &> /dev/null; then
    echo -e "${RED}錯誤: PM2 未安裝${NC}"
    echo "請先執行: npm install -g pm2"
    exit 1
fi

# 主要邏輯
case "$1" in
    "start")
        echo -e "${GREEN}啟動 PM2 服務...${NC}"
        pm2 start ecosystem.config.js
        ;;
    "stop")
        echo -e "${GREEN}停止 PM2 服務...${NC}"
        pm2 stop ecosystem.config.js
        ;;
    "restart")
        echo -e "${GREEN}重啟 PM2 服務...${NC}"
        pm2 restart ecosystem.config.js
        ;;
    "delete")
        echo -e "${GREEN}刪除 PM2 服務...${NC}"
        pm2 delete ecosystem.config.js
        ;;
    "logs")
        echo -e "${GREEN}查看日誌...${NC}"
        pm2 logs
        ;;
    "status")
        echo -e "${GREEN}查看狀態...${NC}"
        pm2 status
        ;;
    "help"|"")
        show_usage
        ;;
    *)
        echo -e "${RED}錯誤: 無效的命令 '$1'${NC}"
        show_usage
        exit 1
        ;;
esac
