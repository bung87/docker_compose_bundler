# docker_compose_bundler  

bundle docker images to tarball base on docker-compose.yml that can then be used with docker load. 

## Installation
`pip install git+http://gitcode.aggso.com/campus/docker_compose_bundler`  
install [pip](https://pip.pypa.io/en/latest/installing/) first if python version less than 2.7.9


## 如何使用？  

`docker_compose_bundler -o bundle.tar` 

output as .xz format:  

`docker_compose_bundler -o  bundle.tar.xz` or  

`docker_compose_bundler -xz -o  bundle.tar`  

for more `docker_compose_bundler -h`
