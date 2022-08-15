```bash
sudo yum update
sudo install docker
sudo systemctl enable docker --now
sudo usermod -aG docker ec2-user
# log out and log in
docker swarm init --advertise-addr 172.31.40.65
# https://dockerswarm.rocks/traefik/#preparation
docker network create --driver=overlay traefik-public
export NODE_ID=$(docker info -f '{{.Swarm.NodeID}}')
docker node update --label-add traefik-public.traefik-public-certificates=true $NODE_ID
export EMAIL=bigbluebutton@ikso.net
export DOMAIN=traefik.testu.eu
export USERNAME=testudo
export HASHED_PASSWORD=$(openssl passwd -apr1)
docker stack deploy -c traefik.yaml traefik
```
