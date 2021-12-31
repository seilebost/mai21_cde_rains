#!/bin/sh

echo "Génération de l image de la fast api"
cd ..
docker image build . -t datascientest/fast_api_cde_rain:1.0.0

echo "Génération de l image image_test_info"
cd tests/repo_test_acces_info
docker image build . -t image_test_info:latest

echo "Génération de l image image_test_predict"
cd ../repo_test_acces_predict
docker image build . -t image_test_predict:latest

echo "Génération de l image image_test_score"
cd ../repo_test_acces_score
docker image build . -t image_test_score:latest

echo "Creation et lancement des containers fast_api_cde_rain / container_test_info / container_test_predict / container_test_score via docker compose"
cd ..
docker-compose up