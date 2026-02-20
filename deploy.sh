#!/bin/bash
# ============================================
# Yael Englander - Server Setup Script
# Run on fresh Ubuntu 22.04 Lightsail instance
# ============================================

set -e

APP_DIR="/var/www/yael"
REPO="https://github.com/boazeng/yaelenglander.git"
DOMAIN="yaelenglander.com"

echo "=== 1. System update ==="
sudo apt update && sudo apt upgrade -y

echo "=== 2. Install dependencies ==="
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git

echo "=== 3. Clone project ==="
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR
git clone $REPO $APP_DIR

echo "=== 4. Setup Python virtual environment ==="
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "=== 5. Setup .env ==="
if [ ! -f "$APP_DIR/.env" ]; then
    cp $APP_DIR/.env.example $APP_DIR/.env
    echo ">>> IMPORTANT: Edit $APP_DIR/.env with your actual API keys!"
fi

echo "=== 6. Setup Nginx ==="
sudo cp $APP_DIR/nginx/yael.conf /etc/nginx/sites-available/yael
sudo ln -sf /etc/nginx/sites-available/yael /etc/nginx/sites-enabled/yael
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

echo "=== 7. Create systemd services ==="

# WhatsApp Agent service
sudo tee /etc/systemd/system/whatsapp-agent.service > /dev/null <<UNIT
[Unit]
Description=WhatsApp Agent (5000)
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/uvicorn tools.5000-whatsapp-connection.whatsapp_agent:app --host 127.0.0.1 --port 5000
EnvironmentFile=$APP_DIR/.env
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT

# Telegram Agent service
sudo tee /etc/systemd/system/telegram-agent.service > /dev/null <<UNIT
[Unit]
Description=Telegram Agent (5001)
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/uvicorn tools.5001-telegram-connection.telegram_agent:app --host 127.0.0.1 --port 5001
EnvironmentFile=$APP_DIR/.env
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT

sudo systemctl daemon-reload
sudo systemctl enable whatsapp-agent telegram-agent
sudo systemctl start whatsapp-agent telegram-agent

echo "=== 8. Setup SSL (after DNS is pointed) ==="
echo "Run this after DNS propagation:"
echo "  sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"

echo ""
echo "=== DONE ==="
echo "Frontend: http://$DOMAIN"
echo "WhatsApp health: http://$DOMAIN/api/whatsapp/health"
echo "Telegram health: http://$DOMAIN/api/telegram/health"
echo ""
echo "NEXT STEPS:"
echo "1. Edit $APP_DIR/.env with your API keys"
echo "2. Point DNS A record to this server's IP"
echo "3. Run: sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo "4. Update WhatsApp webhook URL to https://$DOMAIN/api/whatsapp/webhook"
