# Advancing AI Day Workshop
### AMD Enterprise AI Software Stack — Hands-On Lab (45 Minutes)

**Audience:** Enterprise evaluators and developers new to the AMD AI platform  
**Prerequisites:** A laptop (Linux, macOS, or Windows with WSL), a terminal, and the workshop credentials provided by your facilitator  
**Time:** 45 minutes total

---

## System Setup: Preparing Your Laptop

This workshop uses local terminal commands to install tools and connect to the cluster. The instructions are written for Linux; follow the section for your OS before starting Part 1.

### 🐧 Linux
No additional setup required. Open your terminal and proceed.

### 🪟 Windows — Use WSL (Windows Subsystem for Linux)
All workshop commands must run inside **WSL**, not PowerShell or Command Prompt. If WSL is not already installed:

1. Open **PowerShell as Administrator**
2. Run: `wsl --install`
3. Restart your machine when prompted
4. After restart, open **WSL** (search "Ubuntu" or "WSL" in the Start menu) and complete the Ubuntu first-run setup (create a username and password)

All subsequent terminal commands in this workshop are run inside your WSL terminal.

### 🍎 macOS
Open **Terminal** (Applications → Utilities → Terminal) or a terminal emulator of your choice. The workshop commands run as-is on macOS with one exception: the `kubectl` install step uses a Linux binary URL — see the footnote in Step 2A.

### Required Tools Summary
The tools below are installed during Step 2A. For reference:

| Tool | Purpose | Pre-installed? |
|---|---|---|
| `curl` | Downloads tools and sends API test requests | Yes (Linux, macOS, WSL) |
| `git` | Clones Blueprint source for customization | Usually — if not: `sudo apt install git` (Linux/WSL) or `xcode-select --install` (macOS) |
| `kubectl` | Communicates with the Kubernetes cluster | Installed in Step 2A |
| `helm` | Deploys Kubernetes applications (Blueprints) | Installed in Step 2A |
| `k9s` | Visual terminal dashboard for the cluster | Installed in Step 2A |

---

## What You Will Build Today

In this workshop you will experience the AMD Enterprise AI Software Stack end-to-end — from deploying your first AI model to launching a complete AI-powered medical imaging application.

You will:
1. **Deploy a live AI model** through the AMD AI Workbench — no code required
2. **Observe real-time inference metrics** and chat directly with your running model
3. **Deploy a complete medical imaging AI application** using a Solution Blueprint in a single command
4. **Connect the Blueprint to your model** — seeing how the platform's components snap together
5. **Customize the application** to make it your own

No deep Kubernetes or ML experience required. Every command is explained step by step.

---

## Platform Overview

| Component | What It Does | Why It Matters |
|---|---|---|
| **AMD AI Workbench** | Web UI for deploying, chatting with, and managing AI models | Teams self-serve AI without waiting on IT |
| **AIMs** (AI Inference Microservices) | Pre-packaged, AMD-optimized model servers | Deployment in minutes instead of weeks |
| **Solution Blueprints** | Complete AI applications — UI, backend, and model — in one package | Working starting points; no app dev required |
| **Resource Manager** | Admin UI for clusters, quotas, users, and storage | IT control over who uses what resources |

---

# Part 1: Deploy an AI Model with AMD AI Workbench (15 minutes)

## Why AIMs and AMD AI Workbench?

Before your team can build AI applications, they need access to running AI models. Traditionally this meant weeks of infrastructure work — provisioning servers, installing frameworks, tuning model configs, managing GPU memory.

**AIMs (AMD Inference Microservices)** eliminate all of that. Each AIM is a containerized model server built and optimized by AMD — hardware tuning, memory management, and serving configuration are already done. You pick a model, click Deploy, and it's running.

**AMD AI Workbench** is the self-service portal your data scientists, developers, and engineers use to deploy models, test them, and connect them to applications — with no command-line knowledge required.

---

## Step 1A: Log In to AMD AI Workbench

Open a browser and navigate to the AI Workbench URL provided by your facilitator:

- Format: `https://airmui.<your-domain>` or the IP-based URL on your workshop sheet

Use the login credentials your facilitator provided. After login, confirm you are in the correct **project** — look for the project name in the top navigation bar.

![AMD AI Workbench login page](images/01-overview/login-page.png)

---

## Step 1B: Deploy an AI Model

### Browse the Model Catalog

Click **Models** in the left sidebar. You will see a catalog of available AI models.

![AI Workbench model catalog](images/04-workbench/01-models-catalog.png)

Each card represents an AIM — a model that AMD has pre-packaged with the optimal serving configuration for AMD hardware. You do not need to worry about model weights, GPU configuration, or serving frameworks.

### Start the Deployment

1. Find the model recommended by your facilitator (e.g., **Llama 3.1 8B** or **Mistral 7B**)
2. Click the **three-dot menu (⋮)** in the bottom-right corner of the model card
3. Select **Deploy**

![Model card three-dot menu with Deploy option](images/04-workbench/02-model-card-deploy-menu.png)

### Configure the Deployment

In the **Deployment Settings** panel that appears:

![Deployment configuration panel](images/04-workbench/03-deploy-config-panel.png)

- **Performance metric** — Select **Latency** for this workshop (optimizes for fast, interactive responses)

![Performance metric dropdown](images/04-workbench/04-deploy-performance-dropdown.png)

- **Unoptimized deployment** — Leave this **off**
- If the model shows a **lock icon** (gated model, e.g., Llama family), a Hugging Face authentication section appears. Click **Select existing token** to use the pre-configured workshop token.

![Hugging Face token prompt for gated models](images/04-workbench/05-hf-token-prompt.png)

Click **Deploy**. A confirmation message will appear.

---

## Step 1C: Monitor Your Model and Explore Inference Metrics

### Watch the Deployment

Click **Workloads** in the left sidebar. Find your model — it will show **Pending** or **Starting** initially.

> **What is happening?** The platform is scheduling the model container on a GPU node, pulling the image, and initializing the serving process. This typically takes 3–5 minutes.

Wait for the status to change to **Running** before continuing.

### Explore Live Metrics

Once Running, click **Open details** (or the model name) to see real-time performance data:

| Metric | What It Tells You |
|---|---|
| **Requests/second** | Current query load on the model |
| **Time to First Token (TTFT)** | How quickly the model starts generating a response |
| **Throughput** | Total tokens generated per second |
| **SLO compliance** | Whether the model is meeting its latency Service Level Objectives |

> **Why do SLOs matter?** Enterprise teams commit to response time guarantees for their applications. This dashboard shows whether the model meets those targets — before you put it in production.

### Chat with Your Model

From the model details page, click **Chat** to open a direct conversation interface. Ask a question, evaluate the response quality, and observe the latency.

> **Keep a note of your model's service name** — you will use it in Part 2 to connect the Blueprint. In the Workloads view, click **Connect** on your model card and copy the **Internal URL**. It will look like `http://aim-llm-<model-name>-<id>.svc.cluster.local`.

---

# Part 2: Solution Blueprints — Deploy and Customize a Medical Imaging AI Application (20 minutes)

## Why Solution Blueprints?

Building an AI application from scratch — even with a model already running — still requires writing a UI, a backend, prompt engineering, API wiring, and deployment code. For enterprise teams evaluating use cases, this delay kills momentum.

**Solution Blueprints** eliminate that gap. Each Blueprint is a complete, production-ready AI application distributed as a single deployable package. In this section you will deploy the **MRI Documentation Blueprint** — a full application for AI-assisted medical imaging analysis and report generation.

---

## Step 2A: Open a Terminal and Set Up Tools

All Blueprint deployments use standard Kubernetes tooling from the command line. Open a terminal on your Linux laptop.

> **Why the terminal?** Helm and kubectl are industry-standard tools for deploying applications to Kubernetes. Once you know these two commands, you can deploy any Blueprint — or any Kubernetes application — in seconds.

### Install Required Tools

Run each block of commands in your terminal:

```bash
# Install k9s — a visual Kubernetes dashboard
curl -sS https://webinstall.dev/k9s | bash
source ~/.config/envman/PATH.env
```

> **macOS note:** You can also install k9s via Homebrew: `brew install k9s`

```bash
# Install kubectl — communicates with the Kubernetes cluster
mkdir -p ~/.kube
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

> **macOS note:** Replace `linux/amd64` in the kubectl URL with `darwin/amd64` (Intel Mac) or `darwin/arm64` (Apple Silicon M1/M2/M3). The rest of the command is identical.

```bash
# Install Helm — the package manager used to deploy Blueprints
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Verify all three installed correctly:

```bash
kubectl version --client && helm version && k9s version
```

> **What is Helm?** Helm is like an app store for Kubernetes. AMD Solution Blueprints are packaged as Helm "charts" — you deploy the entire application with a single command instead of managing dozens of individual configuration files.

---

## Step 2B: Connect Your Terminal to the Workshop Cluster

Your facilitator will provide a **kubeconfig file** — a credential file that lets your terminal communicate with the cluster.

Save the kubeconfig content to your machine:

```bash
mkdir -p ~/.kube
nano ~/.kube/demo_write.yaml
# Paste the kubeconfig content your facilitator provided
# Save with: Ctrl+O  →  Enter  →  Ctrl+X
```

Activate it and verify the connection:

```bash
export KUBECONFIG=~/.kube/demo_write.yaml
kubectl get nodes
```

**Expected output:** A list of cluster nodes with `Ready` status. If you see this, your terminal is connected to the cluster.

For a live visual view of the cluster, run `k9s`. Press `:q` to exit.

---

## Step 2C: Deploy the MRI Documentation Blueprint

The **MRI Documentation Blueprint** (`aimsb-mri-docs`) is a complete medical imaging AI application. It provides:
- AI-assisted analysis and summarization of MRI scan reports
- Natural language querying over medical imaging documentation
- Automated report generation for radiologists and clinical teams
- A ready-to-use web interface for healthcare and imaging workflows

### Set Your Variables

Replace the placeholder values with your own. Your facilitator will confirm your namespace.

```bash
name="my-deployment"       # A unique label (use your first name or username)
namespace="my-namespace"   # Your assigned Kubernetes namespace
chart="aimsb-mri-docs"     # The MRI Documentation Blueprint
```

### Deploy

```bash
helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  | kubectl apply -f - -n $namespace
```

> **What does this do?**
> - `helm template` downloads the Blueprint chart from AMD's registry and converts it into Kubernetes configuration files
> - `kubectl apply` sends those configurations to the cluster, creating the application's services, containers, and networking

### Verify the Deployment

```bash
kubectl get pods -n $namespace
```

Pods may show `ContainerCreating` or `Pending` while images pull — this is normal. Run the command again in 2–3 minutes until all pods show **Running**.

You can also run `k9s` and navigate to your namespace for a live view.

![Blueprint deployment in progress](images/blueprints/blueprint-wsl-deployment.png)

### Access the MRI Documentation Application

Once all pods are Running, open a port-forward to view the application:

```bash
kubectl port-forward services/aimsb-mri-docs-$name-ui 7860:7860 -n $namespace
```

Open your browser to **http://localhost:7860**

You should see the MRI Documentation interface. Try uploading a sample report or asking it a question about an imaging study.

> **Note:** Each Blueprint uses a different port. If the above port-forward does not work, check the MRI Documentation Blueprint's `DEPLOYMENT.md` on GitHub for the correct service name and port.

---

## Step 2D: Blueprint Customization — Connect to Your Deployed Model (10 minutes)

By default the Blueprint deployed its own AI model. Now you will reconnect it to **the model you deployed in Part 1**. This is the standard enterprise pattern: one centrally managed model serves multiple applications.

> **Why does this matter?** Running a separate model per application wastes GPU resources and creates management complexity. By pointing Blueprints at a shared AIM, your team gets one model to monitor, update, and scale — and every application benefits automatically.

### Find Your Model's Service Name

Run the following to list all services in your namespace:

```bash
kubectl get svc -n $namespace
```

Look for a service name starting with `aim-llm-`. You can also find it from the Workbench:
1. In AMD AI Workbench, click **Models**
2. On your running model card, click **Connect**
3. Copy the **Internal URL** — the hostname portion is your service name

### Reconnect the Blueprint to Your Model

Replace `<your-model-service-name>` with the service name you found:

```bash
servicename="<your-model-service-name>"   # e.g., aim-llm-meta-llama-3-8b-abc123

helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  --set llm.existingService=$servicename \
  | kubectl apply -f - -n $namespace
```

Wait for pods to restart (`kubectl get pods -n $namespace`), then refresh your browser at **http://localhost:7860**. The MRI Documentation application is now powered by your model from Part 1.

---

### Ideas for Customizing the Blueprint

Bluprints are open-source — the source code is available on GitHub and every component can be modified. Here are some customizations you can explore:

**1. Upgrade the Image Segmentation Model (UNet via MONAI)**

The Blueprint currently segments brain tissue using simple K-means clustering inside `segment_brain_tissue()` in `src/mri_analysis.py`. You can replace this with a deep learning UNet model from a [MONAI bundle](https://monai.io/model-zoo.html) for clinical-grade accuracy — identifying tumor boundaries, organ contours, and tissue types with far greater precision.

First, clone the Blueprint source:

```bash
git clone https://github.com/amd-enterprise-ai/solution-blueprints.git
cd solution-blueprints/solution-blueprints/mri-doc
```

Open `src/mri_analysis.py` and find the `segment_brain_tissue()` function. The current K-means implementation looks like this:

```python
# Current: simple K-means clustering
def segment_brain_tissue(image_array, n_clusters=3):
    pixels = image_array.reshape(-1, 1).astype(np.float32)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(pixels)
    labels = kmeans.labels_.reshape(image_array.shape)
    return labels
```

Replace it with a MONAI UNet inference call:

```python
# Upgraded: MONAI UNet from a pretrained bundle
import torch
from monai.networks.nets import UNet
from monai.transforms import Compose, ScaleIntensity, EnsureChannelFirst, ToTensor

def segment_brain_tissue(image_array, model_path="models/brain_segmentation_unet.pth"):
    # Load pretrained UNet (download bundle from MONAI Model Zoo)
    model = UNet(
        spatial_dims=2,
        in_channels=1,
        out_channels=3,       # 3 tissue classes: CSF, grey matter, white matter
        channels=(16, 32, 64, 128),
        strides=(2, 2, 2),
    )
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    transform = Compose([EnsureChannelFirst(), ScaleIntensity(), ToTensor()])
    input_tensor = transform(image_array).unsqueeze(0)   # add batch dim

    with torch.no_grad():
        output = model(input_tensor)
    labels = output.argmax(dim=1).squeeze().numpy()
    return labels
```

Download a pretrained bundle from the MONAI Model Zoo and save the weights to `models/brain_segmentation_unet.pth`, then rebuild and redeploy the Blueprint container. The application will now use deep learning segmentation on every uploaded scan.

**2. Swap to a Different Language Model**

Change the `llm.existingService` value to point at any other deployed AIM. Try a larger model for more detailed clinical summaries, or a fine-tuned medical language model (e.g., a BioMedLM variant) for domain-specific accuracy. No application code changes needed.

**3. Change the System Prompt**

Each Blueprint exposes prompt configuration. Edit the system prompt to adapt the AI's output style — for example, switching from radiologist-facing technical language to patient-friendly plain-English summaries, or restricting responses to a specific imaging modality (MRI, CT, X-ray).

**4. Deploy a Different Blueprint for Your Use Case**

The same workflow works for any Blueprint:

| Blueprint | Chart Name | Best For |
|---|---|---|
| Document Summarization | `aimsb-docsum` | Summarizing reports and contracts |
| Talk to Your Documents | `aimsb-talk-to-your-documents` | Internal knowledge base Q&A |
| LLM Chat | `aimsb-llm-chat` | Simple chat interface |
| Financial Stock Intelligence | `aimsb-fsi` | Financial analysis and market Q&A |
| Report Generation | `aimsb-report-generation-engine` | Automated report creation |

Change the `chart` variable and re-run the deploy command. You can have multiple Blueprints all pointing to the same shared AIM.

---

# Part 3: Deploy AIMs via CLI (Bonus — if time allows)

The AMD AI Workbench UI is ideal for self-service model deployment, but enterprise platform teams often need to deploy AIMs programmatically — from CI/CD pipelines, scripts, or automation tooling. The **AIM Engine CLI** provides direct Kubernetes-native control over AIM lifecycle.

> **When would you use this?** Scripted deployments, automated scaling triggers, GitOps workflows, or when deploying AIMs to namespaces outside the Workbench's scope.

---

## Step 3A: Understand How AIMs Deploy Under the Hood

Every AIM deployed through the Workbench is backed by a **Kubernetes Custom Resource** of kind `AIMDeployment`. The Workbench UI is simply a front-end for creating and managing these resources. You can create them directly via `kubectl` — giving you the same result without the UI.

A minimal AIM deployment manifest looks like this:

```yaml
apiVersion: aims.amd.com/v1alpha1
kind: AIMDeployment
metadata:
  name: llama-3-8b-cli
  namespace: my-namespace
spec:
  model:
    name: meta-llama/Meta-Llama-3-8B-Instruct
  resources:
    gpus: 1
  performanceProfile: latency
```

---

## Step 3B: Deploy an AIM via kubectl

Make sure your `KUBECONFIG` is set (from Step 2B), then save the manifest and apply it:

```bash
cat <<EOF > aim-deploy.yaml
apiVersion: aims.amd.com/v1alpha1
kind: AIMDeployment
metadata:
  name: llama-3-8b-cli
  namespace: $namespace
spec:
  model:
    name: meta-llama/Meta-Llama-3-8B-Instruct
  resources:
    gpus: 1
  performanceProfile: latency
  huggingFace:
    tokenSecret:
      name: hugging-face-token   # Kubernetes secret created in Resource Manager
      key: HF_TOKEN
EOF

kubectl apply -f aim-deploy.yaml
```

Watch the AIM come up:

```bash
kubectl get aimdeployments -n $namespace
kubectl get pods -n $namespace -l app=llama-3-8b-cli
```

> **What is the controller doing?** The AIM Engine controller watches for `AIMDeployment` resources and automatically creates the underlying vLLM serving pod, service, and metrics endpoint. You never touch the raw pod spec.

---

## Step 3C: Query the AIM Directly

Once the pod is **Running**, you can query the model directly from the terminal — no UI needed:

```bash
# Get the cluster-internal service endpoint
kubectl get svc -n $namespace -l app=llama-3-8b-cli

# Port-forward to your local machine
kubectl port-forward svc/llama-3-8b-cli 8000:8000 -n $namespace &

# Send a test inference request
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Meta-Llama-3-8B-Instruct",
    "messages": [{"role": "user", "content": "Summarize the key benefits of AMD MI300X GPUs in two sentences."}],
    "max_tokens": 150
  }'
```

The response will stream back in OpenAI-compatible format — meaning any application already written for OpenAI's API can point to this endpoint with no code changes.

---

## Step 3D: Tear Down the AIM

```bash
kubectl delete aimdeployment llama-3-8b-cli -n $namespace
```

The controller automatically cleans up all associated pods and services.

---

## CLI vs. UI: When to Use Each

| Scenario | Use |
|---|---|
| Developer / data scientist self-service | **Workbench UI** |
| Automated deployment from CI/CD | **kubectl / AIM Engine CLI** |
| GitOps — model config stored in git | **kubectl apply** with YAML manifests |
| Batch deployment of many models | **kubectl** with a loop or Helm |
| Exploring the catalog and testing models | **Workbench UI** |

---


# Part 4: Fine-Tune a Model on Your Own Data (Bonus — if time allows)

Fine-tuning adapts a general-purpose model to your domain — your terminology, your writing style, your proprietary data. This turns a capable but generic model into one that understands your organization's context and produces outputs that match your standards.

**AMD AI Workbench makes fine-tuning a UI workflow** — no Python, no training scripts, no GPU configuration required. You upload a dataset, select a base model, and the platform handles the rest.

---

## Step 4A: Upload Training Data

Your training data needs to be in **JSONL format** — one JSON object per line, where each object contains a prompt/response pair. A sample dataset is provided by your facilitator at:

```
https://github.com/isab8liu-alum/eai-suite-guides/blob/main/dataset/sft-demo-data.jsonl
```

In AMD AI Workbench:

1. Click **Datasets** in the left sidebar
2. Click **Upload**
3. Fill in:
   - **Dataset name** — e.g., `workshop-demo-data`
   - **Data type** — `.jsonl` / instruction fine-tuning format
4. Select your file and click **Upload**

> **What is in the dataset?** The sample dataset contains instruction-response pairs in the standard SFT (Supervised Fine-Tuning) format. Each entry looks like:
> ```json
> {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
> ```

---

## Step 4B: Start a Fine-Tuning Job

1. Click **Models** in the left sidebar → switch to the **Custom Models** tab
2. Click **Fine-tune model**
3. Configure the fine-tuning job:

| Setting | Value | Notes |
|---|---|---|
| **Base model** | Select the model you deployed in Part 1 | The starting point — your dataset teaches it new behavior |
| **Dataset** | `workshop-demo-data` | The training data you uploaded in Step 4A |
| **Method** | LoRA (Low-Rank Adaptation) | Efficient fine-tuning — adapts the model without retraining all weights |
| **Epochs** | 3 | Number of passes through the training data |
| **Learning rate** | 2e-4 | Leave default for the workshop |

4. Click **Start training**

The fine-tuning job appears in **Workloads** with a **Training** status badge. You can monitor its progress — loss curves and training metrics stream in as it runs.

---

## Step 4C: Deploy and Test Your Fine-Tuned Model

Once training completes, the custom model appears in the **Custom Models** tab.

1. Click **Deploy** on your fine-tuned model — it deploys exactly like any other AIM
2. Wait for status to show **Running**
3. Click **Chat** and ask it questions from the training domain

Compare the fine-tuned model's responses against the base model from Part 1. The fine-tuned model should show noticeably better alignment with your domain terminology and the response style captured in the training data.

---

## Workshop Complete

You have now experienced the AMD Enterprise AI Software Stack end-to-end:

| What You Did | What It Demonstrates |
|---|---|
| Deployed an AI model via Workbench UI | Self-service AI for teams without infrastructure expertise |
| Observed live inference metrics and SLO tracking | Production readiness visibility from day one |
| Deployed a Solution Blueprint with a single Helm command | Complete AI applications in minutes |
| Connected the Blueprint to your model | The platform's composable, shared-model architecture |
| Customized the Blueprint's AI backend | Open-source, modifiable applications |
| Deployed an AIM via kubectl | Programmable, CLI-native model lifecycle management |
| Fine-tuned a model on custom data | Domain adaptation without ML engineering expertise |

**Next steps:**
- Explore additional Solution Blueprints at [AMD Enterprise AI](https://enterprise-ai.docs.amd.com)
- Ask your facilitator about bringing the AMD AI platform to your organization
- Review the [AMD Enterprise AI documentation](https://enterprise-ai.docs.amd.com) for architecture guides and API references
