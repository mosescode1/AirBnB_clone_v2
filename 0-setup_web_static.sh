#!/usr/bin/env bash
# configuring my web servers for deployment
sudo mkdir -p /data/web_static/releases/test/
echo "Hello world EFfa" | sudo tee /data/web_static/releases/test/index.html
sudo ln -s /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/


