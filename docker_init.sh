#!/bin/bash
netowork_name=pgi_network
network_id=$(docker network ls -f "name=$netowork_name" --format "{{.ID}}")

if [ ! $network_id ]
then
  network_id=$(docker network create -d bridge $netowork_name)
  if [ -n "$network_id" ]
  then
    echo "Rede docker '$netowork_name' criada com sucesso!"
  else
    echo "Falha ao criar a rede docker '$netowork_name'!"
  fi
else
  echo "Rede docker '$netowork_name' já criada."
fi
echo "ID: $network_id"

docker-compose up -d