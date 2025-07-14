# deepseek on MI300


# Running DeepSeek-R1 on a single NDv5 MI300X VM

```
az group create --location <REGION> -n <RESOURCE_GROUP_NAME>
az vm create --name mi300x --resource-group <RESOURCE_GROUP_NAME> --location <REGION> --image microsoft-dsvm:ubuntu-hpc:2204-rocm:22.04.2025030701 --size Standard_ND96isr_MI300X_v5 --security-type Standard --os-disk-size-gb 256 --os-disk-delete-option Delete --admin-username azureadmin --ssh-key-values <PUBLIC_SSH_PATH>
```


## perf test
```
evalscope perf \ --url http://xxxxxxx:30000/v1/chat/completions\ --model "deepseek-ai/DeepSeek-R1" \--parallel 5 \--number 20 \--api openai \--min-prompt-length 10000 \--dataset "longalpaca" \--max-tokens 2048 \--min-tokens 2048 \--stream

```