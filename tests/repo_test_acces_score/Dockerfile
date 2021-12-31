FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install flask==1.1.1 && pip3 install requests
ADD test_access_score.py /repo_test_acces_score/test_access_score.py
WORKDIR /repo_test_acces_score/
EXPOSE 5000
CMD python3 test_access_score.py