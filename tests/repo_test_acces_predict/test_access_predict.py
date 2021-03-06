#! /usr/bin/python3
import os
import requests
import os.path as path

# définition de l'adresse de l'API
api_address = '172.50.0.2'
# port de l'API
api_port = 8000

###################################################################################################
# requête numéro 1: tester l'accès aux prédictions avec le modèle SVC et fichier au bon format
###################################################################################################

upload_file1 = {
            "file": ("test.csv", open("/home/api_rain_log/test.csv", "rb"), "text/csv")
        }
r1 = requests.post(
        f"http://{api_address}:{api_port}/predict/SVC",
        headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
        files=upload_file1,
)

output1 = '''
===================================================
    Predict Access test with a valid file format
====================================================

request done at "/predict/SVC"
| "authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="
| file = tests/test.csv
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
# requête numéro 2: tester l'accès aux prédictions avec le modèle SVC et un fichier au mauvais format
###################################################################################################

upload_file2 = {
            "file": ("test.csv", open("/home/api_rain_log/test.csv", "rb"), "text/markdown")
        }
        
r2 = requests.post(
    f"http://{api_address}:{api_port}/predict/SVC",
    headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
    files=upload_file2,
)

output2 = '''
====================================================
    Predict Access test with invalid file format
===================================================

request done at "/predict/SVC"
| "authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="
| file = tests/test.csv
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