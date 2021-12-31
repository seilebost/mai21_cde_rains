echo "Arrêt du container fastapi_data"
docker container stop fastapi_data
echo "Suppression du container fastapi_data"
docker container rm fastapi_data

echo "Arrêt du container container_test_auth"
docker container rm container_test_auth

echo "Arrêt du container container_test_perm"
docker container rm container_test_perm

echo "Arrêt du container container_test_cont"
docker container rm container_test_cont

echo "Suppression des images"

docker image rm image_test_auth 
docker image rm image_test_perm
docker image rm image_test_cont
docker image rm datascientest/fastapi:1.0.0