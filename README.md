# How to Use

## Prerequisites
install nvidia-container-toolkit, see: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

## Start Service
```bash
bash ./start-service.sh flux.1-dev
```
## Request Serivce

```
### openai-image api
```bash
bash ./request-service-openai-image.sh FLUX.1-dev 
```

## Stop Service
```bash
bash ./stop-service.sh flux.1-dev
```

## Table: config-name -> model & api-protocol
| config-name             | model                 | api-protocol |
| ----------------------- | --------------------- | ------------ | |
| flux.1-dev              | FLUX.1-dev            | openai-image |
