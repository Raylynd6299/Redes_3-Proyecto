FROM ubuntu:20.04

LABEL maintainer="RaymundoPB"
LABEL version="1.1"
LABEL description="This is a custom Docker Image for R3-Proy"

RUN apt-get update && apt-get install apt-utils -y
RUN apt-get update && apt-get install sudo iputils-ping iproute2 vim net-tools curl -y
RUN apt-get install openssh-server openssh-client -y

RUN useradd -m UserServer -G sudo

RUN echo "sudo ALL=(ALL:ALL) ALL" > /etc/sudoers
RUN echo "UserServer ALL=NOPASSWD: ALL" > /etc/sudoers

COPY AddIPServer.sh /home/UserServer/

RUN cd /home/UserServer
RUN su UserServer

ENTRYPOINT ["/bin/bash"]
