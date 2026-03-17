# EAI Suite -- Step‑by‑Step Installation & Usage Guide

> **AMD Official Use Only -- AMD Internal Distribution Only**\
> Beginner-friendly walkthrough for installing and using the EAI Suite
> on AMD Developer Cloud.

------------------------------------------------------------------------

## Overview

This guide walks complete beginners through installing, configuring, and using the **AMD Enterprise AI Suite** on AMD Developer Cloud.

### Target Audience

- AMD Business Development
- Field Engineers
- Future end users

### Prerequisites

- Basic Linux command-line knowledge
- Familiarity with SSH
- AMD Developer Cloud access

------------------------------------------------------------------------

# 1. Installation of EAI Suite

## DigitalOcean Installation (AMD Developer Cloud)

### Step 1 — Create a GPU droplet

1. Navigate to [AMD Developer Cloud GPU Droplets](https://amd.digitalocean.com/gpus/).
2. Create an **MI300X GPU Droplet**.

> ⚠️ If selecting 8x GPUs, cost = `8 × $1.99/hour`

------------------------------------------------------------------------

### Step 2 — Download Cluster Bloom

SSH into the droplet or click the Web Console button.

Paste in terminal the following commands
```bash
wget https://github.com/silogen/cluster-bloom/releases/latest/download/bloom
chmod +x bloom
```

------------------------------------------------------------------------

### Step 3 — Get Droplet IP

Copy the Public IPv4 droplet IP address from AMD Developer Cloud.

------------------------------------------------------------------------
### Step 4 — Create the Bloom Configuration File - Option 1 via GUI

In terminal type :
```bash
./bloom
```

This opens the Cluster Bloom configuration UI. Select the **Medium t-shirt size** (recommended for a single 8-way node), then proceed with the installation. Select and input other corresponding parameters.
### Step 4 — Create the Bloom Configuration File

Create and open a configuration file called `bloom.yaml`:

```bash
nano bloom.yaml
```

Paste the following configuration, replacing `<your-ip-address>` with your droplet's IP address:

```yaml
DOMAIN: <droplet-ip-addr>.nip.io
FIRST_NODE: true
GPU_NODE: true
CLUSTER_DISKS: /dev/vdc1
CERT_OPTION: generate
```

------------------------------------------------------------------------

### Step 5 — Start the Installation

Run the following command to begin the installation:

```bash
sudo ./bloom cli bloom.yaml
```

Upon completion, it will provide two URLs for you to access via Keycloak authentication. (See Step 7)

------------------------------------------------------------------------

### Step 6 — Reload the shell

Once the installation completes, either exit and re-login to your SSH session, or run:

```bash
source ~/.bashrc
```

------------------------------------------------------------------------

### Step 7 — Authenticate via Keycloak

Visit:

    https://kc.<your-ip-address>.nip.io

Then open:

    https://airmui.<your-ip-address>.nip.io

#### Default Credentials

| Field    | Value                                      |
|----------|--------------------------------------------|
| Username | `devuser@<your-ip-address>.nip.io`         |
| Password | `password`                                 |

You should now see the **AMD Resource Manager Dashboard**.

------------------------------------------------------------------------

## Installing AMD Enterprise AI Suite On Premises

This guide walks you through installing [AMD Enterprise AI Suite](https://enterprise-ai.docs.amd.com/en/latest/platform-infrastructure/on-premises-installation.html) on a single node. The installation uses a tool called **Cluster Bloom**, which sets up a Kubernetes cluster and installs the platform for you.

*For the full installation reference, including TLS certificate options, and backup and restoration, see the [official documentation](https://enterprise-ai.docs.amd.com/en/latest/platform-infrastructure/on-premises-installation.html).*

### Prerequisites

Before you begin, ensure your environment meets the prerequisites defined on the [documentation page](https://enterprise-ai.docs.amd.com/en/latest/platform-infrastructure/on-premises-installation.html#prerequisites).

### Installation

#### Step 1 — Download Cluster Bloom

SSH into your node as root and run the following command to download the Cluster Bloom installation tool:

```bash
wget https://github.com/silogen/cluster-bloom/releases/latest/download/bloom
```

Make the installation script executable:

```bash
chmod +x bloom
```

------------------------------------------------------------------------

#### Step 2 — Create the Bloom Configuration File

Create and open a configuration file called `bloom.yaml`:

```bash
vi bloom.yaml
```

For the standard installation, you should use the default values provided in the documentation, the only exception is the DOMAIN and OIDC_URL values which should match your specific domain name. In this example we are using a `nip.ip` domain -> Replace `<your-ip-address>` with your server's IP address in the `DOMAIN` and `OIDC_URL` fields:

```yaml
DOMAIN: <your-ip-address>.nip.io
CERT_OPTION: generate
FIRST_NODE: true
GPU_NODE: true
USE_CERT_MANAGER: false
CLUSTER_DISKS: /dev/vdc1
OIDC_URL: https://kc.<your-ip-address>.nip.io/realms/airm
```

If you do not have a DNS-enabled domain, you can use a `.nip.io` domain, which automatically resolves to your server's IP address. A `.nip.io` domain is created for you as part of the installation process. For more details on domain configuration, see the [official documentation](https://enterprise-ai.docs.amd.com/en/latest/platform-infrastructure/on-premises-installation.html#domain-names).

------------------------------------------------------------------------

#### Step 3 — Start the Installation

Run the following command to start the installation:

```bash
sudo ./bloom --config bloom.yaml
```

This launches the Cluster Bloom wizard web interface. Follow the on-screen instructions for access:

1. If you are accessing the server remotely, create an SSH tunnel. The required command is displayed at the bottom of the terminal output.
2. Once the tunnel is established, copy and paste the provided URL into your web browser. This opens the Cluster Bloom configuration wizard.
3. Review your configuration in the wizard. You can modify the domain name, storage settings, TLS certificates, and other advanced options such as the OIDC provider.
4. Once you are happy with the configuration, you can click on the installation button.

You can monitor the progress in the web interface.

**Note:** You can also run the installation with CLI confirmation instead of the wizard:

 ```bash
 sudo ./bloom cli --config bloom.yaml
 ```

------------------------------------------------------------------------

#### Step 4 — Monitor the Installation

The Kubernetes installation is finished when the UI shows that all steps are 100% complete, and the terminal confirms that the “Installation completed successfully”. Once the cluster is operational, the application installation begins automatically.

View the installation in Kubernetes by reloading the shell environment:

```bash
source ~/.bashrc
```

Then launch k9s:

```bash
k9s
```

------------------------------------------------------------------------

#### Step 5 — Log in

Verify the installation by logging in to the AMD Enterprise Suite web interface:

- Access the login URL for your domain:
  - For a `.nip.io` domain: `https://airmui.<master-node-ip-address>.nip.io`
  - For a registered domain: `https://airmui.<your-domain>`
- Log in with the username `devuser@domain` and the default password `password`. You will be prompted to change the password on first login.

You should now see the **AMD Resource Manager Dashboard**.

------------------------------------------------------------------------

#### Step 6 — Add your Hugging Face token 

A Hugging Face token is required to download gated models. You can add it directly through the AMD AI Workbench UI when deploying or fine-tuning a model — the token is stored securely as a Kubernetes secret.

------------------------------------------------------------------------

# 2. AMD Resource Manager

## Overview

AMD Resource Manager provides platform administrators with tools to oversee and control the platform's computational resources and user access. Key capabilities include cluster management, monitoring, and maintaining teams' access to computational resources.

### Core Concepts

- **Dashboard**: High-level overview of your clusters, resource allocations, and basic utilization statistics
- **Projects**: Create and manage projects, which organize and isolate work within your system. Project settings include user membership, secrets, storage, and quotas
- **Quota**: Guaranteed resource quota for a project to ensure fair resource allocation
- **Storage**: Configurations providing credentials and connectivity information for storage (e.g., S3)
- **Secrets**: Secure information such as API keys or credentials assigned to projects
- **Users**: Manage users, their roles, and their project membership

------------------------------------------------------------------------

## Setting Up a Project

### Step 1 — Navigate to Resource Manager

1. From the **Dashboard**, navigate to the **Projects** page
2. Click on the **Create project** button
3. Enter the project name, a description, and then select your cluster 
4. Click on **Create project**

> Your project is now created and ready for configuration.

------------------------------------------------------------------------

### Step 2 — Adjusting Quota

You should now be directed to the **Project settings** page and the **Quota** section. Quotas ensure fair and shared resource allocation across projects.

Determine the amount of ensured resources needed for your project:
1. GPUs - Number of GPU devices
2. CPU Cores - Number of CPU cores
3. System Memory - Memory allocation
4. Ephemeral Disk - Ephemeral disk space
5. Click on **Save changes**

------------------------------------------------------------------------

### Step 3 — Attaching Storage Secret

During installation a minio-credentials-fetcher secret is created and a storage is setup, for each project to be able to download and run workloads a storage needs to be in place.


1. Navigate to the **Secrets** tab
2. Click **Add project secret** and select **Assign existing secret**
3. Select the **minio-credentials-fetcher** secret from the **Secret** drop-down menu
4. Click **Assign secret**, you should now see that the secret is added

------------------------------------------------------------------------

### Step 4 — Adding Users to the Project

Users must be added to projects to be able to access the project and the computational resources.

1. Click on the **Users** tab, located next to storage
2. Click the **Add Member** button
3. Select yourself (and any other desired user) from the **Users** drop-down menu
4. Click **Add to project**

> Your project is now configured and ready to be used.

------------------------------------------------------------------------

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

# 4. Blueprints

Solution Blueprints are reference applications built with AIMs. Solution Blueprints offer an easy way to explore AIMs in the context of a complete microservice solution. For developers, Solution Blueprints act as starting points and example implementations, making it fast and easy to solve real-world needs with ROCm software.

Documentation page can be found [here](https://enterprise-ai.docs.amd.com/en/latest/solution-blueprints/overview.html).

## Launching Blueprints Helm Charts

Solution Blueprints are provided as Helm Charts. The recommended approach to deploy them is to pipe the output of helm template to `kubectl apply -f -`. We don’t recommend helm install, which by default uses a Secret to keep track of the related resources. Ensure you have access to the cluster trough the terminal. Access guide can be found [here](https://enterprise-ai.docs.amd.com/en/latest/resource-manager/workloads/accessing-the-cluster.html#constructing-the-kubeconfig-file).

```bash
name="my-deployment"
namespace="my-namespace"
chart="aimsb-my-chart"
helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  | kubectl apply -f - -n $namespace
```

## Using an existing deployment or external LLM

By default, any required AIMs are deployed by the helm chart. If you already have a compatible AIM deployed, you can use that instead, and reuse resources.

To use an existing deployment or external model, set the corresponding `existingService` value to that endpoint. You should use the Kubernetes Service name, or if the service is in a different namespace, you can use the long form <SERVICENAME>.<NAMESPACE>.svc.cluster.local:<SERVICEPORT>. If needed, you can pass a whole URL.

Full example command:

```bash
name="my-deployment"
namespace="my-namespace"
chart="aimsb-my-chart"
servicename="aim-llm-my-model-123456"
helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  --set llm.existingService=$servicename \
  | kubectl apply -f - -n $namespace
```

------------------------------------------------------------------------

# 5. Troubleshooting

## DigitalOcean Installation Issues

Common causes: 

------------------------------------------------------------------------

## Cluster Bloom Issues

### Configuration Failed or Timed Out

Try rerunning Bloom:

``` bash
sudo ./bloom cli --config bloom.yaml
```

If issue persists: - Verify disk mapping (`/dev/vdc1`) - Ensure droplet
has sufficient resources - Confirm network access

------------------------------------------------------------------------

# Appendix

### Useful Commands

``` bash
kubectl get pods -A
kubectl get svc -A
kubectl describe pod <pod-name>
```

------------------------------------------------------------------------

------------------------------------------------------------------------

**Maintained by AMD -- Internal Documentation**
