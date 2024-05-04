#!/usr/bin/env bash
# configuring my web servers for deployment
sudo apt-get update -y
sudo apt-get -y install nginx
sudo service nginx start
new_string="server_name _;\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}"
string2=" root /data/web_static/current/;"
sudo mkdir -p /data/web_static/releases/test/
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html
if [ -L /data/web_static/current ];
then
        sudo rm -rf /data/web_static/current
fi

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i "s#server_name _;#$new_string#"  /etc/nginx/sites-enabled/default
sudo sed -i "s#root /var/www/html/;#$string2#"  /etc/nginx/sites-enabled/default
sudo service nginx reload