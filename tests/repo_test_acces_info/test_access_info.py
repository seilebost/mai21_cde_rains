#! /usr/bin/python3
import os
import requests
import os.path as path

# définition de l'adresse de l'API
api_address = '172.50.0.2'
# port de l'API
api_port = 8000

###################################################################################################
# requête numéro 1: tester l'accès aux infos avec un bon user
###################################################################################################

r1 = requests.get(
    f"http://{api_address}:{api_port}/info",
    headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
)

output1 = '''
==========================================
    Info Access test with a valid-user
==========================================

request done at "/info"
| "authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="
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

###################################################################################################
# requête numéro 2: tester l'accès aux infos avec un format invalide
###################################################################################################

r2 = requests.get(
    f"http://{api_address}:{api_port}/info",
    headers={"authorization-header": "Basic wrongb64str"},
)

output2 = '''
====================================================
    Info Access with invalid base64 string
===================================================

request done at "/info"
| "authorization-header": "Basic wrongb64str"
expected result = 400
actual restult = {status_code}

==>  {test_status}

'''

# statut de la requête
status_code = r2.status_code

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output2.format(status_code=status_code, test_status=test_status))
print("la variable est : ",str(os.environ.get('LOG')))



# impression dans le fichier de la log
if str(os.environ.get('LOG')) == "1":
    with open('/home/api_rain_log/log.txt', 'a') as file:
        file.write(output2.format(status_code=status_code, test_status=test_status))

###################################################################################################
# requête numéro 3: tester l'accès aux infos avec un user non habilité
###################################################################################################

r3 = requests.get(
    f"http://{api_address}:{api_port}/info",
    headers={"authorization-header": "Basic dXNlcjpwYXNzd29yZA=="},
)

output3 = '''
====================================================
    Info Access with wrong user
===================================================

request done at "/info"
| "authorization-header": "Basic dXNlcjpwYXNzd29yZA=="
expected result = 403
actual restult = {status_code}

==>  {test_status}

'''

# statut de la requête
status_code = r3.status_code

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output3.format(status_code=status_code, test_status=test_status))
print("la variable est : ",str(os.environ.get('LOG')))

# impression dans le fichier de la log
if str(os.environ.get('LOG')) == "1":
    with open('/home/api_rain_log/log.txt', 'a') as file:
        file.write(output3.format(status_code=status_code, test_status=test_status))