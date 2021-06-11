FROM ubuntu:18.04
RUN apt update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install flask requests
COPY . /root/AddTask_ECS_Microservice/
WORKDIR /root/AddTask_ECS_Microservice/
EXPOSE 5000
CMD ["python3","addtask.py"]
