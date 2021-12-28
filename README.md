# API Machine Learning

Il s'agit de la mise en place d'une API de Machine Learning sous KUBERNETES.
ATTENTION : le paramétrage du port IP d'accès à l'API est `8002`

## Partie DOCKER

### Compilation de l'image fast_api_cde_rain 
docker image build . -t datascientest/fast_api_cde_rain:1.0.0

### Test de l'api seul via docker
docker container run -p 8000:8000 datascientest/fast_api_cde_rain:1.0.0
la commande `curl -X GET http://0.0.0.0:8000` doit retourner `{"status":"running"}` 

## Partie KUBERNETES

### Lancement de minikube
`minikube start`

### Lancement du dashboard
`minikube dashboard --url=true`

### Vérification de la présence de kubectl
`kubectl version --client`

### Accès en local du dashboard
`kubectl proxy --address='0.0.0.0' --disable-filter=true`
retourne par exemple `http://127.0.0.1:36351/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/` : remplacer 127.0.0.1 par l'adresse IP publique du poste et remplacer le port 36351 par 8001

### Déploiement de notre API via la ligne de commande

* Création du déploiement dans KUBERNETES : `kubectl create -f k8s-deployment-cde-rain.yml`
* Vérification du déploiement : `kubectl get deployment`

Si le déploiement est KO, vérifier que l'image docker est bien déployée dans le docker local de KUBERNETES : voir la FAQ ci-dessous pour vérifier et corriger.

### Exposition de l'API par SERVICE via la ligne de commande

`kubectl expose deploy deploie-projet-cde-rain --type=ClusterIP --port=8002 --target-port=8000 --name service-projet-cde-rain`

### Exposition de notre API à l'extérieur du cluster via la ligne de commande

* Création de l'exposition : `kubectl create -f k8s-ingress-cde-rain.yml`
* Récupération du paramétrage pour accèder à l'API : `kubectl get ingress`

### Vérification du bon fonctionnement

ssh -i "data_enginering_machine.pem" ubuntu@adresseIPpersonnelle -fNL 8002:192.168.49.2:80
puis sur un navigateur :
`http://localhost/docs` pour avoir la documentation de l'API
`http://localhost/` pour avoir le statut de l'API (running si disponible dans KUBERNETES)

## F.A.Q.

### Vérifier que l'image DOCKER à tester est bien dans le docker local de KUBERNETES
`minikube ssh` puis `docker images`

### Rendre local l'image docker dans KUBERNETES
`eval $(minikube docker-env)`
puis
`docker image build . -t datascientest/fast_api_cde_rain:1.0.0`
Vérification de l'image dans le depôt de KUBERNETES 
`minikube ssh` puis `docker images`

Puis vérifier dans le dashboard de KUBERNETES que le déploiement est devenu OK


