#! /usr/bin/python3
import os
import requests
import os.path as path

# définition de l'adresse de l'API
api_address = '172.50.0.2'
# port de l'API
api_port = 8000

###################################################################################################
# requête : tester l'accès au score
###################################################################################################

r1 = requests.post(
            f"http://{api_address}:{api_port}/score",
            headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
            json={"model_name": "SVC"},
        )

output1 = '''
==========================================
    Score Access test 
==========================================

request done at "/score"
| "authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="
| "model_name": "SVC"
expected result = 200
actual restult = {status_code}

==>  {test_status}

'''


# statut de la requête
status_code = r1.status_code

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output1.format(status_code=status_code, test_status=test_status))
print("la variable est : ",str(os.environ.get('LOG')))

# impression dans le fichier de la log
if str(os.environ.get('LOG')) == "1":
    with open('/home/api_rain_log/log.txt', 'a') as file:
        file.write(output1.format(status_code=status_code, test_status=test_status))