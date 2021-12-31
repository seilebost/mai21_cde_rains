FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install flask==1.1.1 && pip3 install requests
ADD test_access_info.py /repo_test_acces_info/test_access_info.py
WORKDIR /repo_test_acces_info/
EXPOSE 5000
CMD python3 test_access_info.py