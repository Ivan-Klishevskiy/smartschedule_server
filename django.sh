#!/bin/bash
echo "Build docker-compose"
docker-compose build

echo "Up docker-compose"
docker-compose up
