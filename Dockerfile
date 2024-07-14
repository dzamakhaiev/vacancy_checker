FROM selenium/standalone-chrome
ENV CHECK_INTERVAL_MINUTES 30

RUN sudo apt-get update
RUN sudo apt-get install git -y
RUN sudo apt-get install python3 -y
RUN sudo apt-get install python3-pip -y
RUN sudo git clone --depth 1 https://github.com/dzamakhaiev/vacancy_checker.git

VOLUME ["/vacancy_checker/logs"]
VOLUME ["/vacancy_checker/database"]

WORKDIR /vacancy_checker
RUN sudo pip3 install -r requirements.txt
COPY email_data.txt email_data.txt
CMD sudo git pull && sudo python3 main.py