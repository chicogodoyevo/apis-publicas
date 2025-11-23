#!/bin/bash
echo "Atualizando pacotes do sistema..."
sudo sudo apt-get update
echo "Atualizando certificados de segurança..."
sudo apt-get install --reinstall ca-certificates
sudo update-ca-certificates

echo "Criando ambiente virtual..."
python3 -m venv venv
echo "Criando ambiente virtual..."
source venv/bin/activate
echo "Instalando dependências..."
pip3 install -r requirements.txt
echo "Ambiente configurado! Para ativar o ambiente virtual, use: source venv/bin/activate"