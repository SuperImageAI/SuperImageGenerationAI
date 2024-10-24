# Quick Start

## Model deployment

### Prerequisites

install nvidia-container-toolkit, see: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

### Start Service

```bash

git clone https://github.com/SuperImageAI/SuperImageGenerationAI.git

cd dockerFile

bash ./start-service.sh flux.1-dev
```

### Request Serivce

```
### openai-image api
```bash
bash ./request-service-openai-image.sh FLUX.1-dev 
```

### Stop Service

```bash
bash ./stop-service.sh flux.1-dev
```

### Table: config-name -> model & api-protocol

| config-name | model      | api-protocol |
| ----------- | ---------- | ------------ |
| flux.1-dev  | FLUX.1-dev | openai-image |

## Deploy the DBC AI public chain worker node

For details, see the work Node Deployment section in the Node Deployment section below：

https://github.com/DeepBrainChain/AIComputingNode

### Download executable program Add execution permission

  chmod +x host_v0.1.6_linux_amd64

### Generate worker.json Configuration File

 ./host_v0.1.6_linux_amd64 -init worker

### Configure the work.json file to add the boot node

 For example, see the workNodeFile/worker.json file

### Run worker node

nohup ./host_v0.1.6_linux_amd64 -config ./worker.json >/home/AI_project/AIComputingNode/AIComputingNode/log/workerdbc3log_$(date +\%Y-\%m-\%d-\%H).log 2>&1&


## Model registration on the DBC AI public chain

curl -X POST http://127.0.0.1:7002/api/v0/ai/project/register
    -H "Content-Type: application/json"
    -d '{
           "project": "SuperImageAI",
           "models": [
             {
               "model": "FLUX.1-dev",
               "api": "http://127.0.0.1:1042/v1/images/generations",
               "type": 1
             }
           ]
         }'
