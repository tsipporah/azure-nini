# Deepseek 32B/70B SGLang
```
Env :
Driver https://us.download.nvidia.com/tesla/550.54.15/nvidia-driver-local-repo-ubuntu2204-550.54.15_1.0-1_amd64.deb

Cuda 12.4
https://developer.nvidia.com/cuda-12-4-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local

python3 -m sglang.launch_server --model-path /home/azureuser/DeepSeek-R1-Distill-Qwen-32B --port 30000 --mem-fraction-static 0.9 --tp 4 --trust-remote-code --host 0.0.0.0
```


# Deepseek 32B/70B VLLM

```
python3 benchmark_serving.py 
  --backend vllm 
  --model /home/azureuser/deepseek-ai/DeepSeek-R1-Distill-Llama-70B 
  --served-model-name deepseek-r1-70b 
  --base-url http://0.0.0.0:8080 
  --endpoint /v1/completions
  --dataset-name sharegpt 
  --dataset-path /home/azureuser/ShareGPT_V3_unfiltered_cleaned_split/ShareGPT_V3_unfiltered_cleaned_split.json 
  --request-rate 200
  --max-concurrency 128 
  --num-prompts 1000 
  | tee bench128_200_vllm.log
```
