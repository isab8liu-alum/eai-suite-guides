# Advancing AI Day Workshop
### AMD Enterprise AI Suite — Hands-On Lab (45 Minutes)

**Audience:** Enterprise evaluators and developers new to the AMD AI platform  
**Prerequisites:** A Linux laptop, a terminal, and the workshop credentials provided by your facilitator  
**Time:** 45 minutes total

---

## What You Will Build Today

In this workshop you will experience the AMD Enterprise AI Suite end-to-end — from deploying your first AI model to launching a complete AI-powered medical imaging application.

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

```bash
# Install kubectl — communicates with the Kubernetes cluster
mkdir -p ~/.kube
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

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

Blueprints are open-source starting points — here are some quick wins you can explore after the workshop:

**1. Swap to a Different Image Segmentation Model**  
The MRI Documentation Blueprint can be configured to use a specialized image segmentation AIM instead of the default language model. Image segmentation models identify and label distinct regions within an MRI scan — for example, detecting tumor boundaries, organ contours, or tissue types.

To swap in a segmentation model, deploy a segmentation AIM from the Workbench catalog (look for models tagged `vision` or `segmentation`, such as a SAM or MedSAM variant), then update the Blueprint to use it:

```bash
segmentation_service="aim-segmentation-<model-id>"   # your deployed segmentation AIM

helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  --set segmentation.existingService=$segmentation_service \
  | kubectl apply -f - -n $namespace
```

With a segmentation model connected, the application can highlight anatomical structures directly on the scan images in addition to generating text reports.

**2. Swap to a Different Language Model**  
Change the `llm.existingService` value to point at any other deployed AIM. Try a larger model for more detailed clinical summaries, or a fine-tuned medical language model (e.g., a BioMedLM variant) for domain-specific accuracy.

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

# Part 3: Fine-Tune a Model on Your Own Data (Bonus — if time allows)

Fine-tuning adapts a general-purpose model to your domain — your terminology, your writing style, your proprietary data. The Workbench makes this accessible without any ML engineering background.

## Step 3A: Upload Training Data

In AMD AI Workbench:

1. Click **Datasets** in the left sidebar
2. Click **Upload**
3. Use the sample dataset provided by your facilitator:  
   `https://github.com/isab8liu-alum/eai-suite-guides/blob/main/dataset/sft-demo-data.jsonl`

![Dataset upload interface](images/04-workbench/uploading_dataset_finetuning.png)

4. Fill in:
   - **Dataset name** — e.g., `workshop-demo-data`
   - **Data type** — `.jsonl` / instruction fine-tuning format
   - **Description** — optional
5. Upload the file and click **Upload**

## Step 3B: Start Fine-Tuning

1. Click **Models** → switch to the **Custom Models** tab

![Custom Models view](images/04-workbench/workbench_custom_models_view.png)

2. Click **Fine-tune model**

![Fine-tune model configuration panel](images/04-workbench/finetune_model_menu.png)

3. Configure:
   - **Base model** — Select the model you deployed in Part 1
   - **Dataset** — Select `workshop-demo-data`
   - **Training parameters** — Leave defaults for the workshop
4. Click **Start training**

The fine-tuning job appears in **Workloads**. Once complete, your custom model is available in the catalog and can be deployed as an AIM — then pointed to by any Blueprint using `llm.existingService`.

---

# Wrap-Up

## What You Accomplished

In 45 minutes you:

- **Deployed a live AI model** through the Workbench UI — no infrastructure expertise needed
- **Observed real-time SLO metrics** for a production-grade model deployment
- **Deployed the MRI Documentation Blueprint** with a single Helm command
- **Connected the Blueprint to your model** — demonstrating resource sharing across applications
- **Explored customization paths** for adapting Blueprints to real enterprise use cases
- **Started a fine-tuning job** on custom data (bonus)

## Quick Reference Commands

```bash
# Set variables
name="my-deployment"
namespace="my-namespace"
chart="aimsb-mri-docs"
servicename="aim-llm-<your-model-service>"

# Deploy a Blueprint (with its own model)
helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  | kubectl apply -f - -n $namespace

# Redeploy pointing to an existing AIM
helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  --set llm.existingService=$servicename \
  | kubectl apply -f - -n $namespace

# Check pod status
kubectl get pods -n $namespace

# Port-forward to access the MRI Documentation Blueprint
kubectl port-forward services/aimsb-mri-docs-$name-ui 7860:7860 -n $namespace

# List services in your namespace
kubectl get svc -n $namespace

# Remove a Blueprint
helm template "$name" "oci://registry-1.docker.io/amdenterpriseai/$chart" \
  | kubectl delete -n "$namespace" -f -

# Visual cluster dashboard
k9s
```

## Next Steps

| Goal | Resource |
|---|---|
| Explore more Blueprints | [Solution Blueprints Overview](https://enterprise-ai.docs.amd.com/en/latest/solution-blueprints/overview.html) |
| Browse the full AIM catalog | [AIMs Catalog](https://enterprise-ai.docs.amd.com/en/latest/aims/aims_catalog.html) |
| Install the platform | [Installation Guide](https://enterprise-ai.docs.amd.com/en/latest/index.html) |
| CLI and automation (AIM Engine) | [AIM Engine Docs](https://enterprise-ai.docs.amd.com/en/latest/aims/aim-engine/overview.html) |

---

*AMD Enterprise AI Suite — Advancing AI Day Workshop | enterprise-ai.docs.amd.com*
