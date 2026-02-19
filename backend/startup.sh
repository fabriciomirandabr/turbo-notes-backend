#!/bin/bash
set -e

apt-get update
apt-get install -y python3-pip python3-venv git

cd /opt
git clone https://github.com/fabriciomirandabr/turbo-notes-backend.git app || (cd app && git pull)
cd app

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export SECRET_KEY="$(openssl rand -base64 32)"
export DEBUG=False

python manage.py migrate --noinput

# Create systemd service
cat > /etc/systemd/system/turbo-backend.service << 'EOF'
[Unit]
Description=Turbo Notes Backend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/app
Environment=SECRET_KEY=change-me-in-production
Environment=DEBUG=False
ExecStart=/opt/app/venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8080 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable turbo-backend
systemctl start turbo-backend
