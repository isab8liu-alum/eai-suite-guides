# 3. AMD Workbench

## Finetuning

Finetuning allows customers to adapt base models to domain-specific
data.

### Typical Workflow

1.  Add Hugging Face token
2.  Upload dataset
3.  Select base model
4.  Configure training parameters
5.  Launch finetuning job

------------------------------------------------------------------------

## Deploy AIM

1. Navigate to the **Models** tab to access the AIM catalog
2. Go to the model card and click the three-dot menu in the bottom-right corner
3. Select **Deploy**
4. Choose a configuration:
   - **Default** — automatically selects the best metric for your model and hardware
   - **Latency** — prioritize low end-to-end latency
   - **Throughput** — prioritize sustained requests/second
   - **Unoptimized deployment** — deploy to hardware the AIM is not specifically optimized for
5. If the model is gated (indicated by a lock icon, e.g., Llama family), you will be prompted for a Hugging Face token. Either select a pre-existing token or add one directly.
6. Click **Deploy** to start the workload. You will receive confirmation that the workload has started.

------------------------------------------------------------------------

## VSCode (vLLM Benchmarking)

### Launch VSCode

1.  Navigate to **Workspaces**
2.  Click **View and deploy** (Visual Studio)
3.  Onced deployed, click on the **Launch** button

### Example: Benchmarking

**Note:** This is an example benchmarking script. Depending on the model and workload characteristics, adjustments may be required.

Steps:
1. Deploy the AIM to benchmark (see section above).
2. Once deployed, find the endpoint:
  - Go to the model card and click the three-dot menu in the bottom-right corner.
  - Click **Connect**.
  - Copy the **Internal URL**. Since the workspace runs inside the cluster, use the Internal URL. If accessing from outside the cluster (e.g. locally), use the **External URL** together with an API key.
3. Open the Visual Studio Code workspace and run the commands below in the terminal.

```bash
python --version # Check Python

python -m venv venv # Create Python virtual environment

source venv/bin/activate # Activate Python virtual environment

pip install vllm # Install vllm
```

Then run (feel free to create a bash script for easier customization):

```bash
NUM_PROMPTS=<number-of-prompts>
CONC=$((NUM_PROMPTS * 10))
INPUT_LEN=<input-token-length>
OUTPUT_LEN=<output-token-length>
BASE_URL="<your-internal-url>"
ENDPOINT="/v1/chat/completions"
MODEL="<your-model-name>"

vllm bench serve \
  --ignore-eos \
  --backend openai-chat \
  --base-url "${BASE_URL}" \
  --endpoint "${ENDPOINT}" \
  --model "${MODEL}" \
  --dataset-name random \
  --random-input-len ${INPUT_LEN} \
  --random-output-len ${OUTPUT_LEN} \
  --num-prompts ${NUM_PROMPTS} \
  --max-concurrency ${CONC} \
  --trust-remote-code
```

### Understanding Output Metrics

| Metric     | Meaning                      |
|------------|------------------------------|
| Throughput | Tokens processed per second  |
| TTFT       | Time to First Token          |
| Latency    | Request processing delay     |
| Tokens/sec | Generation speed             |

------------------------------------------------------------------------

## ComfyUI

ComfyUI enables: 
- Visual AI workflow creation 
- Image generation pipelines 
- Model experimentation via UI

------------------------------------------------------------------------

