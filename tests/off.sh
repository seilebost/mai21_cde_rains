echo "Arrêt du container fast_api_cde_rain"
docker container stop fast_api_cde_rain
echo "Suppression du container fast_api_cde_rain"
docker container rm fast_api_cde_rain

echo "Arrêt du container container_test_info"
docker container rm container_test_info

echo "Arrêt du container container_test_predict"
docker container rm container_test_predict

echo "Arrêt du container container_test_score"
docker container rm container_test_score

echo "Suppression des images"

docker image rm datascientest/fast_api_cde_rain:1.0.0 
docker image rm image_test_info
docker image rm image_test_predict
docker image rm image_test_score