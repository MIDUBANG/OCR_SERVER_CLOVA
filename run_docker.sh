# echo killing old docker processes
# docker-compose rm -fs
#!/bin/bash

# Installing docker engine if not exists
if ! type docker > /dev/null
then
  echo "docker does not exist"
  echo "Start installing docker"
  sudo apt-get update
  sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
  sudo apt update
  apt-cache policy docker-ce
  sudo apt install -y docker-ce
fi

# Installing docker-compose if not exists
if ! type docker-compose > /dev/null
then
  echo "docker-compose does not exist"
  echo "Start installing docker-compose"
  sudo curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

echo "start docker-compose up: ubuntu"
echo "i'm in bash file. my bucket name is ${AWS_ACCESS_KEY}"
AWS_ACCESS_KEY = $AWS_ACCESS_KEY
AWS_SECRET_KEY = $AWS_SECRET_KEY
BUCKET_NAME = $BUCKET_NAME
X_OCR_SECRET = $X_OCR_SECRET
sudo docker-compose -f /home/ubuntu/src/clova/docker-compose.yml up --build -d 


# echo building docker containers
# sudo docker-compose up --build -d