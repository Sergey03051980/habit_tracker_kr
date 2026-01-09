#!/bin/bash
echo "🔧 Настройка сервера для Docker деплоя..."

# 1. Обновление системы
sudo apt update && sudo apt upgrade -y

# 2. Установка Docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 3. Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# 5. Настройка firewall
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw --force enable

echo "✅ Сервер настроен!"
echo "📋 Далее:"
echo "   1. git clone репозиторий в /opt/habit_tracker"
echo "   2. Добавить .env файл"
echo "   3. docker-compose up -d"
