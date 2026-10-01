# Taiwan ODM Workshop
### AMD Enterprise AI Software Stack, AIMs, and Blueprints — Hands-On Labs (90 Minutes)

**Audience:** Enterprise IT administrators, platform engineers, and team leads evaluating the AMD AI platform<br>
**Prerequisites:** A browser, workshop credentials, and either Windows 10/11, native Ubuntu/Debian Linux, or macOS<br>
**Time:** 90 minutes total<br>
**Terminal use:** Module 1 uses browser-based tools. Module 2 uses your laptop terminal; Windows participants use the Ubuntu WSL terminal.

## Workshop Access

Use the following workshop portals and your assigned participant number:

| Portal | URL |
|---|---|
| **AMD AI Workbench** | [https://aiwbui.amd-workshop.silogen.ai/](https://aiwbui.amd-workshop.silogen.ai/) |
| **AMD Resource Manager** | [https://airmui.amd-workshop.silogen.ai/](https://airmui.amd-workshop.silogen.ai/) |
| **Kubernetes API** | `https://k8s.amd-workshop.silogen.ai` |

- **Username:** `userN@amd-workshop.silogen.ai` — replace `N` with your assigned number (for example, `user1@amd-workshop.silogen.ai`)
- **Password:** Use the password provided by the workshop facilitator
- **Project:** Select the project assigned to your participant number, or the project specified by the facilitator
- **Namespace:** Use the namespace assigned by the facilitator, typically `projN` for `userN`

---

## System Setup: Preparing Your Laptop

Module 1 runs in the browser, including its in-cluster VSCode benchmark. Module 2 adds local Kubernetes and Helm commands. When you reach Module 2, use its OS routing table and follow only the Windows/WSL, native Linux, or macOS path that matches your laptop.

---

## What You Will Learn Today

This workshop takes you deep into the administrative and operational capabilities of the AMD Enterprise AI Software Stack through its two main management interfaces.

You will:
1. **Kubernetes Concepts - Slides**
2. **Deploy and manage the GPT-OSS-20B AIM** through AMD AI Workbench — observe live inference metrics, configure autoscaling, and chat with the running model
3. **Benchmark a deployed model in VSCode** — measure throughput, latency, and time to first token with `vllm bench serve`
4. **Explore AMD Resource Manager** — view node GPU metrics and the admin control plane for projects, quotas, secrets, and storage
5. **Deploy an AIM with kubectl** — use a CLI-native Kubernetes workflow
6. **Deploy and customize a Solution Blueprint** — connect a medical imaging application to an AIM and expose it through HTTPS routing

No prior Kubernetes or ML engineering experience is required. Each browser and local-terminal step is explained in sequence.

---

## Platform Overview

| Component | What It Does | Who Uses It |
|---|---|---|
| **AMD AI Workbench** | Self-service UI for deploying models and running development workspaces | Data scientists, developers, and engineers |
| **AIMs** (AI Inference Microservices) | Pre-packaged AMD-optimized model servers | Deployed and managed through both UIs |
| **Workspaces** | JupyterLab, VSCode, or ComfyUI environments that run inside the cluster | End users running experiments or tools |
| **AMD Resource Manager** | Admin UI for clusters, projects, quotas, users, secrets, and storage | IT admins and platform operators |

---

# Part 1: AMD AI Workbench — Model Deployment and Autoscaling (20 minutes)

## Why Workbench?

**AMD AI Workbench** is the self-service portal for AI practitioners — data scientists, developers, and engineers who need to deploy models, run experiments, and collaborate on AI workloads without needing Kubernetes or infrastructure expertise.

---

## Step 1A: Log In to Workbench and Select Your Project

Open a browser and navigate to AMD AI Workbench:

- [https://aiwbui.amd-workshop.silogen.ai/](https://aiwbui.amd-workshop.silogen.ai/)


Sign in as `userN@amd-workshop.silogen.ai`, replacing `N` with your assigned participant number. Use the password provided by the facilitator. After login, confirm you are in the correct project by checking the project name in the top navigation bar.

![AMD AI Workbench login page](aai_workshop_images/login-page.png)

Then select your project from the dropdown

![AMD AI Workbench select project page](aai_workshop_images/workbench-project-select-dropdown.png)

---

## Step 1B: Deploy an AI Model

### Browse the Model Catalog

Expand **Models** in the left sidebar and click **AIM Catalog**. You will see a catalog of available AIMs — AMD-packaged model servers for a range of model families.

![AI Workbench model catalog](aai_workshop_images/wb-aim-catalog.png)

Each card shows the model name, publisher, accelerator type, and version count. AMD has pre-configured the serving stack, hardware tuning, and memory layout for each — you do not configure any of this manually.

### Deploy Your Model

1. Find **GPT OSS 20B** in the AIM Catalog. This is the AIM used throughout this workshop.
2. Click the **Deploy** button on the model card.

![Model card with Deploy button](aai_workshop_images/wb-model-card-deploy.png)

> **Note:** You may see fewer models than shown here. Administrators control which models are available to each user, so your catalog will only display the models you have been granted access to.

> **Why GPT-OSS instead of Llama for this lab?** Llama model repositories are gated — shown with a **Gated** badge on the card. Before deploying a Llama AIM, a user must accept the model's access terms on Hugging Face and provide an authorized Hugging Face token, normally through a pre-configured project secret. GPT-OSS-20B avoids that gated-model prerequisite for this workshop. Do not select a Llama AIM unless the facilitator confirms that access and the token are ready.

### Configure the Deployment

Clicking **Deploy** opens the **Model Deployment** wizard, which walks through four steps — **Model**, **Deployment**, **Scaling**, and **Check**. Use **Next** to advance and **Back** to revise; the wizard does not deploy anything until you press **Submit** on the final step.

#### Step 1 — Model

Confirm the model and pick a **Container version**. Leave the default **(Latest)** for this workshop. **Image pull secrets** can be left empty for ungated models like GPT OSS 20B.

![Deployment wizard — Model step](aai_workshop_images/wb-deploy-wizard-1-model.png)

#### Step 2 — Deployment

Optionally give the deployment a **Name**, then choose a **Performance metric**:

![Deployment wizard — Deployment step](aai_workshop_images/wb-deploy-wizard-2-deployment.png)

| Option | What It Does |
|---|---|
| **Latency** | Prioritize low time-to-first-token — **select this for the workshop** |
| **Throughput** | Prioritize sustained requests per second |
| **Advanced profile selection** | Choose the serving profile manually |

**Latency** is selected by default. Once chosen, the platform resolves the matching hardware profile for you — for GPT OSS 20B that is **fp4** precision on **MI350X × 1**, optimization class **Optimized**.

#### Step 3 — Scaling

The **Scaling** step is marked **Optional**. For this workshop, leave **Enable autoscaling** toggled **off** and click **Next**.

![Deployment wizard — Scaling step](aai_workshop_images/wb-deploy-wizard-3-scaling.png)

This step also shows a running summary of the **Model** and **Deployment** choices you made, each with an **Edit** button if you need to go back.

> **Important — GPU capacity limit:** Leave autoscaling **off** for this workshop. Each participant project has a limited GPU quota shared across the lab environment; if the autoscaler tries to schedule replicas beyond that quota, the workload hangs in a pending state and never runs. See [Autoscaling — Optional Reference](#autoscaling--optional-reference) after Step 4 if you want to explore it in the developer zone.

#### Step 4 — Check

The final step summarizes everything before anything is created. Confirm the values match the table below, then click **Submit**.

![Deployment wizard — Check step](aai_workshop_images/wb-deploy-wizard-4-check.png)

| Field | Expected Value |
|---|---|
| **Model** | GPT OSS 20B |
| **Container version** | 0.11.1 (Latest) |
| **Performance metrics** | Latency |
| **Precision** | fp4 |
| **Accelerator** | MI350X × 1 |
| **Optimization class** | Optimized |
| **Autoscaling** | Disabled |

> **Nothing is deployed until you click Submit.** You can safely open the wizard and page through all four steps to explore the options, then **Cancel** or close it without consuming any GPU quota.

After you click **Submit**, continue to Step 1C to watch the deployment start.

---

### Autoscaling — Optional Reference

> **Not part of the workshop path.** Leave autoscaling disabled for this lab; this section is reference material for your own environment.

Autoscaling automatically adjusts the number of running model replicas based on real-time demand — scaling up during traffic spikes and back down during low usage, so you only consume GPU resources when you need them.

> **Important:** Autoscaling must be enabled **at deployment time** — you cannot enable it on an existing deployment. If it was enabled at deploy time, you can update its parameters later via **Settings** on the workload detail page.

#### Enable Autoscaling at Deploy Time

To enable autoscaling, toggle **Enable autoscaling** on in the **Scaling** step of the deployment wizard, which expands the parameters below:

![Autoscaling configuration panel](aai_workshop_images/autoscaling.png)

Configure the following parameters:

| Parameter | Recommended Value | What It Does |
|---|---|---|
| **Min replicas** | 1 | Minimum replicas always running — ensures baseline capacity even at zero traffic |
| **Max replicas** | **1** | Upper bound — prevents runaway resource use; constrained by your project's GPU quota |
| **Scaling metric** | Running requests (default) | The vLLM signal used to drive scaling decisions |
| **Aggregation** | Average (default) | How metric values are combined across all running pods |
| **Target type** | Absolute value (default) | How the target threshold is interpreted |
| **Target value** | 10 (default) | Scale up when total running requests across all pods exceed this number |

> **Important — GPU capacity limit:** If you do enable autoscaling in the developer zone, set **Max replicas to 1**. Each participant project has a limited GPU quota shared across the lab environment. If you set a higher max, the autoscaler may attempt to schedule additional replicas that exceed your quota — the workload will hang in a pending state and never run.

#### How It Works

- The platform evaluates the scaling metric every **30 seconds**
- **Scale-up:** When demand exceeds your target threshold, additional replicas are added (up to your configured maximum)
- **Scale-down:** When demand drops below the threshold and stays low through a **5-minute cooling period**, replicas are removed (down to your configured minimum) — the cooldown prevents flapping

#### Scaling Metric Options

| Metric | When to Use |
|---|---|
| **Running requests** (default) | Stable, reactive scaling based on active load — good for most workloads |
| **Waiting requests** | Proactive scaling that reacts before latency degrades — triggers on queue buildup before response times increase |

> **How autoscaling interacts with quotas:** Autoscaling scales within your project's GPU quota. If your quota allows 4 GPUs and each replica uses 1, autoscaling can create up to 4 replicas. When autoscaling borrows resources beyond a project's guaranteed quota, those pods may be preempted if other projects reclaim their allocation.

You can generate controlled request load later using the `vllm bench serve` test in Part 2 and compare the results with the live metrics in the Workloads tab.

---

## Step 1C: Monitor Your Model — Live Inference Metrics

### Watch the Deployment Start

Click **Dashboard** in the left sidebar. Your model will show **Pending** or **Starting** while the platform schedules it on a GPU node and initializes the serving process. This typically takes 3–5 minutes.

> **What is happening under the hood?** The platform is creating a Kubernetes pod on an AMD GPU node, pulling the AIM container image, and starting the vLLM serving process. GPU memory allocation and model weight loading happen during this initialization window.

Wait for the status to change to **Running**.

### Explore Live Metrics

Once the model is running, go to **Models → Deployed Models**, click the **three-dot menu (⋮)** at the right of the model row, and select **Open details** to view the real-time metrics dashboard:

![Deployed model actions menu](aai_workshop_images/wb-deployed-model-actions.png)

The same menu provides **Chat with model**, **Connect to model**, and **Undeploy** — all three are used later in this workshop.

| SLA Metric | What It Tells You |
|---|---|
| **Inference Requests** | Current inference load on the model |
| **Time to First Token (TTFT)** | Latency from request submission to first token generated |
| **Throughput (tokens/sec)** | Total generation rate across all concurrent requests |
| **End-to-end latency** | Total time from request submission to the complete response being generated |
| **GPU Utilization** | Hardware utilization — helps right-size the deployment |

> **Why do Metrics matter?** Enterprise applications commit to response time guarantees. For example, a customer-facing AI assistant might require TTFT < 500ms.

### Chat with Your Model

Open the chat interface in either of two ways:

- From **Models → Deployed Models**, click the **three-dot menu (⋮)** on the model row and select **Chat with model**, or
- Click **Chat** in the left sidebar and pick your deployment from the **Select model** dropdown at the top right.

Either route opens the Chat view with your deployment already selected. The model selector shows the deployment's resolved configuration — container version, performance metric, accelerator, and precision — so you can confirm you are talking to the right instance.

Type a question in the message box and press **Enter**:

![Chat with the deployed GPT OSS 20B model](aai_workshop_images/wb-chat-with-model.png)

Ask a question and observe:
- The response latency (TTFT)
- The quality of the response
- How the metrics dashboard updates in real time as you generate traffic

> **Tip:** The **Compare** tab next to **Chat** lets you send the same prompt to several deployments side by side — useful for weighing a smaller, faster AIM against a larger one. The gear icon opens generation settings such as temperature and max tokens.

---

# Part 2: Benchmarking with vLLM Bench Serve in VSCode (15 minutes)

The AMD AI Workbench includes browser-based development workspaces connected to the cluster. You will use its VSCode workspace to benchmark the GPT-OSS-20B AIM deployed in Part 1 without installing tools on your laptop.

## Why Benchmark?

Deploying a model is only the first step. Before committing to a production configuration, you need to understand how the model performs under realistic load:

- What is the maximum throughput?
- Does latency stay within SLO at 10 concurrent users? 50? 100?
- At what concurrency does latency degrade or throughput stop increasing?

The `vllm bench serve` tool measures real-world model performance — throughput, latency, and time to first token — under realistic load. Use this to validate model performance before production use.

---

## Step 2A: Find and Copy Your GPT-OSS Model Endpoint

First, collect the connection information for the GPT-OSS-20B model that you deployed in Part 1. You will use it after launching VSCode in Step 2B.

In AMD AI Workbench:

1. Expand **Models** in the left sidebar and click **Deployed Models**.
2. Find the running **GPT-OSS-20B** deployment (status **Running**).
3. Open its **three-dot action menu (⋮)** and select **Connect to model**. This opens the connection dialog.

![Connect to model dialog](aai_workshop_images/wb-connect-to-model.png)

4. Copy the **Internal URL**. It looks like `http://wb-aim-<id>-<id>-predictor.<namespace>.svc.cluster.local`. Use the internal URL because the VSCode workspace runs inside the same platform.
5. Copy the exact **model ID** shown in the code snippet (for this workshop, `openai/gpt-oss-20b`). Do not guess it from the display name.
6. In the dialog's **CODE SNIPPET** box, toggle **Use internal URL** on, select the **Python** tab, and click the **Copy** icon in the upper-right corner. Keep this copied code available; you will paste it into a Python file in Step 2B.

> **Toggle "Use internal URL" before copying.** The snippet defaults to the external gateway URL. Flipping the toggle rewrites the snippet to use the cluster-internal address, which is what the VSCode workspace needs.

> **Replace the API key placeholder.** The generated snippet contains `UPDATE_YOUR_API_KEY_HERE`. Substitute a key you create under **API Keys** in the left sidebar.

> **Internal versus external URL:** The **Internal URL** is reachable only from inside the cluster — use it from the VSCode workspace. The **Inference URL** is the unified AI gateway, reachable from outside the cluster, and requires an API key. Use the **Internal URL** for this workshop.

> **Shortcut:** The same dialog has an **Open in chat** button, which opens the Chat view with this deployment preselected.

> **Reference:** Follow AMD's [Find model endpoints](https://enterprise-ai.docs.amd.com/en/latest/workbench/inference/how-to-deploy-and-inference.html#find-model-endpoints) instructions for the **Connect** dialog, URL selection, Python tab, and copy button.

---

## Step 2B: Launch a VSCode Workspace

Click **Workspaces** in the left sidebar, then click on the VSCode workspace card (or **Create Workspace** → VSCode).

In the workspace configuration panel:

![Workspace custom resource allocation](aai_workshop_images/workspace-deploy-custom-resource-allocation.png)

- **Name** — e.g., `bench-workspace`
- **CPU/Memory** — leave defaults for the workshop
- **GPU** — set to `0` for the benchmarking workspace (the benchmark sends HTTP requests; it does not need a GPU itself)
- **Storage** — the workspace comes with a persistent home directory

Click **Create**. The workspace status will show **Starting** — typically 1–2 minutes.

Once **Running**, click **Open** to launch VSCode in your browser.

> **What makes this different from a local VSCode?** The workspace runs inside the same Kubernetes cluster as your models. You can reach model services directly by their internal cluster hostname — no port-forwarding or VPN required. Your work is also persistent: files saved in the workspace home directory survive workspace restarts.

### Prepare Python and Test the Endpoint with curl

In VSCode, select **Terminal → New Terminal** (or press `` Ctrl+` ``). Create a Python virtual environment and install the package used by the Python sample:

```bash
python --version
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install requests
```

> **Expected result:** The virtual environment activates and `requests` installs without errors. If `python -m venv` reports that `venv` or `ensurepip` is unavailable, stop and ask the facilitator to use a workspace image with Python virtual-environment support. Do not install operating-system packages or use `sudo` inside the managed workspace unless the facilitator explicitly authorizes it.

> **Python interpreter check:** Keep the virtual environment active and run Python with `python`, not `/bin/python`. Confirm the selected interpreter with `command -v python`; it should point to the `venv/bin/python` created above. An explicit `/bin/python` bypasses the virtual environment and will not see the `requests` package installed there.

Set the endpoint and model values copied in Step 2A:

```bash
export BASE_URL="<your-gpt-oss-internal-url>"
export MODEL="<your-gpt-oss-model-id>"

# Remove a trailing slash if one was copied.
export BASE_URL="${BASE_URL%/}"
```

Confirm that the endpoint is reachable and that it advertises the expected model:

```bash
curl --fail-with-body --silent --show-error \
  "${BASE_URL}/v1/models" | python -m json.tool
```

Check that the JSON response contains your model ID in the `data` list. Then send a simple chat-completion request:

```bash
curl --fail-with-body --silent --show-error \
  -X POST "${BASE_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d "$(printf '{\"model\":\"%s\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello, world!\"}],\"max_tokens\":64}' "$MODEL")" \
  | python -m json.tool
```

> **Expected result:** The command returns HTTP success and a JSON object containing `choices`. The model's reply appears under `choices[0].message.content`. The exact wording will vary, but it should respond to **Hello, world!**.

### Create and Run a Python File

Save the test as `/workload/test.py` so it can be run with the Python environment included in the VSCode workspace:

1. Click the **Explorer** icon in the VSCode activity bar on the left, or press `Ctrl+Shift+E`.
2. Select the `/workload` folder in the Explorer. Click the **New File** icon next to the folder name.
3. Enter `test.py` and press `Enter`. The complete file path should be `/workload/test.py`.
4. Paste the Python sample that you copied from the model's **Connect** dialog in Step 2A.
5. Confirm that the sample uses the copied **Internal URL** and exact model ID. Change the user-message `content` to `Hello, world!`.
6. Save the file with `Ctrl+S`.
7. Return to the VSCode terminal. Install `requests` into the workspace's built-in Python environment, then run the file with that same interpreter:

```bash
/opt/venv/bin/python -m pip install requests
/opt/venv/bin/python /workload/test.py
```

Using the same `/opt/venv/bin/python` path for both commands ensures that `test.py` can import the installed `requests` package. The response should contain a `content` field with the model's reply. If the copied sample does not use the environment variables above, replace its endpoint URL and model value directly with the values copied in Step 2A.

If `curl` or Python reports that the host cannot be resolved, confirm that you used the **Internal URL** and that you are running inside the Workbench VSCode workspace, not on your laptop. If the server reports that the model does not exist, check `/v1/models` and use the exact returned `id` value.

---

## Step 2C: Run the Benchmark

Keep using the terminal and virtual environment from Step 2B. If you opened a new terminal, reactivate the environment and set `BASE_URL` and `MODEL` again. Then install the benchmarking tool:

```bash
source venv/bin/activate
python -m pip install vllm
```

> **Expected result:** `vllm` installs without errors. Do not continue until the endpoint test in Step 2B succeeds.

Create `bench_serve.sh` with the benchmark procedure used in the Workbench guide. It reuses the exported `BASE_URL` and `MODEL` values:

```bash
cat > bench_serve.sh <<'EOF'
NUM_PROMPTS=20
CONC=10
INPUT_LEN=1024
OUTPUT_LEN=1024
ENDPOINT="/v1/chat/completions"

: "${BASE_URL:?Set and export BASE_URL before running this script}"
: "${MODEL:?Set and export MODEL before running this script}"

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
EOF

chmod +x bench_serve.sh
./bench_serve.sh
```

> **What do these parameters mean?**
> - `NUM_PROMPTS` controls the total requests sent
> - `CONC` caps simultaneous requests; reduce it if the shared workshop environment is busy
> - `INPUT_LEN` and `OUTPUT_LEN` set the synthetic prompt and response token lengths
> - `MODEL` must match the model ID served by your GPT-OSS endpoint

![vLLM bench serve output](aai_workshop_images/bench_serve.png)

---

## Step 2D: Interpret the Benchmark Output

The benchmark prints measured results from your deployment. Do not compare runs unless the model, prompt lengths, output lengths, request count, concurrency, and serving configuration are the same.

| Metric | Meaning | What to Look For |
|---|---|---|
| **Throughput** | Total tokens processed per second across all requests | Higher is better for batch workloads |
| **TTFT** | Time to First Token — how quickly the model starts responding | Lower is better for interactive use; compare P99 with your SLO |
| **Latency** | End-to-end time per request | Lower is better; compare equivalent workload settings |
| **Tokens/sec** | Per-request token generation rate | Higher means faster completions per user |

> **Exercise:** Change `NUM_PROMPTS` and `CONC`, re-run the benchmark, and compare throughput and TTFT. Use the Workbench metrics page to correlate client-observed results with the live service metrics.

## Cleanup: Undeploy GPT-OSS-20B

After completing the benchmark, undeploy GPT-OSS-20B to release its GPU allocation:

1. In the Workbench left sidebar, click **Models**
2. Select the **Deployed Models** tab
3. Find your GPT-OSS-20B deployment and click the **⋮** (three-dot menu)
4. Click **Undeploy** (shown in red)

![Undeploy AIM from Workbench](aai_workshop_images/workbench-undeploy-AIMs.png)

> **Note:** Undeploying stops the model and releases the GPU allocation back to your project quota. Any running inference requests will be terminated.

---

# Part 3: AMD Resource Manager — Platform Administration (10 minutes)

## Why Resource Manager?

In enterprise environments, AI infrastructure is shared. Multiple teams — data science, engineering, product — all want access to GPUs. Without governance, one team can accidentally consume all cluster resources, leaving others blocked.

**AMD Resource Manager** is the administrative control plane. It lets IT administrators:
- Monitor GPU metrics for individual cluster nodes over selectable time ranges
- Create isolated **projects** for each team or use case
- Set **resource quotas** (GPU hours, memory, storage) per project
- Manage **user access** and assign roles
- Store and distribute **secrets** (API keys, model tokens) securely
- Attach **persistent storage** for datasets and model artifacts

In this section you will tour the user workflow. Your instructor will also demo the administrator workflow

---

## Step 3A: Log In to Resource Manager

Open a browser and navigate to AMD Resource Manager:

- [https://airmui.amd-workshop.silogen.ai/](https://airmui.amd-workshop.silogen.ai/)

Sign in as `userN@amd-workshop.silogen.ai`, replacing `N` with your assigned participant number. Use the password provided by the facilitator.

![Resource Manager dashboard overview](aai_workshop_images/01-dashboard-overview-rm.png)

The dashboard has two sections:

**Clusters and Nodes** — summary cards showing the number of clusters, GPU nodes, available GPUs, and allocated GPUs across the cluster.

**Allocations and Workloads** — a **Consumption by project** table listing each project's GPU allocation, GPU utilization, running workloads, and pending workloads. Summary cards on the right show total GPU Utilization, Running Workloads, and Pending Workloads across all projects.

---

## Step 3B: View GPU Metrics for a Node

1. Click **Clusters** in the left sidebar, then open the workshop cluster.
2. In the nodes table, select a GPU node to open its detail page.
3. Scroll to **Device metrics**.
4. Use the device selector to filter the charts to a specific GPU, or leave the default selection to view all available devices.
5. Use the time-range selector to view data from the last **1 hour**, **24 hours**, or **7 days**.

Explore the available charts for the selected device and time range. The controls are shared across the GPU metric views, so you can change the filter once and review the charts without configuring each one separately.

> **Reference:** AMD Enterprise AI documentation: [Node GPU Metrics](https://enterprise-ai.docs.amd.com/en/latest/resource-manager/clusters/node-metrics.html).

---

## Step 3C: Explore the Projects Page

Projects are the primary isolation boundary. Each team or use case gets its own project with its own quota, users, secrets, and storage.

Click **Projects** in the left sidebar to see all projects in the cluster.

![Resource Manager projects page](aai_workshop_images/rm-projects-page-view-only.png)

The projects list shows every project provisioned on the cluster, with a summary of its resource allocation:

| Column | What It Shows |
|---|---|
| **Project** | The project name — typically named by team, use case, or workshop participant |
| **Status** | Whether the project is **Ready** (fully provisioned and accepting workloads) |
| **GPU Allocation** | Number of GPUs allocated to the project and what share of total cluster GPU capacity that represents |
| **CPU Allocation** | CPU cores allocated, shown as a count and cluster percentage |
| **Memory Allocation** | RAM allocated, shown in GB and cluster percentage |

> **Admin demo only — Creating projects:** Your account has read access to the Projects page. Creating and managing projects is an administrator function. Your facilitator will now demonstrate how to create a new project, set its name and description, and assign it a resource quota.

---

## Step 3D: Explore Your Project

Double-click your assigned project in the list to open its detail view.

![Project overview page](aai_workshop_images/user-project-view-page.png)

The project overview shows live resource consumption at a glance:

| Panel | What It Shows |
|---|---|
| **Workloads in project** | Total workload count and their current states (Running, Pending, etc.) |
| **Wait Time (Avg)** | How long workloads have been waiting for GPU resources to become available |
| **Quota Utilization (Avg)** | How much of the project's guaranteed quota is currently in use |
| **GPU Idle Time (Avg)** | Time GPUs have been allocated but not actively computing — useful for identifying waste |
| **GPU Device Usage** | Current number of GPUs in active use |
| **GPU VRAM Usage** | Memory consumed across allocated GPUs, shown against the project's total allocation |

The **Workloads** table at the bottom lists every running or queued job in the project — name, type, status, GPU count, VRAM, creation time, run duration, and the user who submitted it.

---

## Step 3E: View Resource Quotas

To view quota settings, click the **Actions** button in the top-right corner of the project page.

![Project actions menu](aai_workshop_images/user-project-actions-menu.png)

> **Note — Limited permissions:** As a team member, you will see the tooltip *"Team Members can only view the project and its resources."* The **Edit settings** and **Delete** options are visible but restricted. Select **Edit settings** to open the Project settings in read-only mode.

In the **Project settings** panel, click the **Quota** tab.

![Quota settings — read-only view](aai_workshop_images/user-project-quota-view-only.png)

The quota table shows two values for each resource:

| Column | What It Means |
|---|---|
| **Guaranteed Allocation** | Resources reserved exclusively for this project — always available, even when the cluster is busy |
| **Available to Allocate** | Slack capacity across the cluster that this project could temporarily use if demand spikes |

> **Understanding quota enforcement:** The platform supports *quota bursting* — a project can temporarily use slack cluster capacity beyond its guaranteed allocation when additional resources are available. However, **when the cluster is under contention, no project can exceed its guaranteed quota and displace another team's workloads.** The guaranteed allocation is both the floor your team is assured and the enforced ceiling under contention.

> **Note:** The Project settings panel also includes **Secrets**, **Storage**, **Users**, and **Details** tabs. As a team member, you can view the contents of these tabs but cannot make changes.

### Admin demo — Configuring Quotas and Managing Secrets

The steps below are performed by a **cluster administrator**. Your account does not have permission to complete them, but please follow along as your facilitator demonstrates.

**Quota configuration (admin only)**

Administrators set the guaranteed resource allocation for each project from the same **Quota** tab you just viewed. They can adjust GPU, CPU, memory, and disk limits at any time — changes take effect immediately and apply to all subsequent workloads in the project.

**Secrets (admin only)**

Secrets let administrators distribute credentials — such as a Hugging Face API token for gated models — to all workloads in a project without users ever handling the raw token value.

From the **Secrets** tab, an admin clicks **Add** → **Hugging Face Token**:

![Secrets tab with Add dropdown](aai_workshop_images/06-secrets-tab-add-menu.png)

In the dialog, the admin provides a name and pastes the token:

![Create secret dialog](aai_workshop_images/07-assign-secret-dialog.png)

Once saved, the token value is never shown again in the UI. The secret appears in Workbench's deployment panel whenever a gated model requires authentication — users can use the secret without ever seeing its value.

![Secret successfully created](aai_workshop_images/08-secret-assigned.png)

For teams that need access to shared dataset or model artifact storage, admins can also assign object storage credentials under **Add** → **MinIO / S3 Compatible**. If the credentials already exist at the cluster level, the admin assigns them to the project from a list rather than re-entering the values:

![Assign MinIO secret to project](aai_workshop_images/07-assign-secret-minio.png)

The resulting secret is mounted as environment variables into authorized workspaces and model deployments — workloads access the bucket automatically without users handling raw credentials.


---

## Module 1 Complete

You have now experienced the full administrative and operational lifecycle of the AMD Enterprise AI Software Stack:

| What You Did | What It Demonstrates |
|---|---|
| Deployed an AI model and observed live metrics | Production visibility from the first deployment |
| Reviewed autoscaling controls and quota limits | Dynamic resource efficiency under variable load |
| Benchmarked GPT-OSS-20B from a VSCode workspace | Quantified throughput and latency before production commitment |
| Toured Resource Manager — node GPU metrics, projects, quotas, and secrets | Infrastructure visibility, IT governance, and multi-team resource control |

**Continue:** Proceed to Module 2 below for the CLI AIM and Solution Blueprint labs.

---

# Module 2: AIMs and Solution Blueprints

This module requires CLI deployment. Complete Module 1 first, then continue here.

## Module 2: What You Will Build

In this workshop you will experience the AMD Inference Microservices (AIMs) and Solution Blueprints — from deploying a healthcare focused AI application to customizing and extending it.

You will:
1. **Deploy an AIM via kubectl** — the CLI-native approach for launching a model on the cluster (llama-3.2-1b-instruct)
2. **Deploy a reference medical imaging AI application** using a Solution Blueprint — pointed directly at the AIM you just deployed
3. **Customize the Blueprint** — tear down the initial deployment and redeploy it with default AIM

No deep Kubernetes or ML experience required. Every command is explained step by step.

---

## Module 2 System Setup: Choose the Section for Your Laptop

This module uses local terminal commands. Follow **only** the path for your laptop operating system:

| Laptop OS | Go to |
|---|---|
| **Windows 10/11** | Step 1A, **Path A1** to install Ubuntu with WSL, then **Path A2** for the consolidated WSL tool installation |
| **Native Ubuntu/Debian Linux** | Step 1A, **Path A2** only |
| **macOS** | Step 1A, **Path B** for the consolidated macOS tool installation |

> **Important:** Do not mix commands between paths. Windows users must run the workshop's Linux commands inside the **Ubuntu WSL terminal**, not PowerShell, Command Prompt, Rancher Desktop's WSL distribution, or Git Bash.

---
## Platform Overview

| Component | What It Does | Why It Matters |
|---|---|---|
| **AIMs** (AI Inference Microservices) | Pre-packaged, AMD-optimized model servers | Deployment in minutes instead of weeks |
| **Solution Blueprints** | Complete AI applications — UI, backend, and model — in one package | Working starting points; no app dev required |

---

# Module 2 — Part 1: Deploy an AIM via kubectl (15 minutes)

Enterprise platform teams often deploy AIMs programmatically from CI/CD pipelines, scripts, or automation tooling. In this lab you will deploy a minimal AIM service with standard Kubernetes `Deployment` and `Service` manifests.

> **When would you use this?** Scripted deployments, automated scaling triggers, GitOps workflows, or workshop namespaces that are already prepared by a platform administrator.

---

## Step 1A: Install WSL and Set Up All Required Tools

Choose the path that matches your laptop. **Run one path only.**

### Path A1 — Windows Only: Install Ubuntu with WSL

Skip this path if Ubuntu already appears when you run `wsl --list --verbose`.

1. Confirm that the laptop runs Windows 10 version 2004 or later, or Windows 11.
2. Open **PowerShell as Administrator**.
3. Install WSL with the Ubuntu distribution:

```powershell
wsl --install -d Ubuntu
```

4. Restart Windows if prompted.
5. Open **Ubuntu** from the Start menu. On first launch, create the Linux username and password requested by Ubuntu.
6. In PowerShell, confirm Ubuntu is installed and then open that exact distribution:

```powershell
wsl --list --verbose
wsl.exe -d Ubuntu
```

Continue in the **Ubuntu terminal** with Path A2. Do not run the next script in PowerShell.

> If `wsl --install` only displays help or cannot find Ubuntu, run `wsl --list --online`, then retry `wsl --install -d Ubuntu`. Ask the facilitator before using a different distribution.

### Path A2 — Ubuntu WSL or Native Ubuntu/Debian Linux: Run One Installation Script

Windows participants run this entire block inside the Ubuntu WSL terminal. Native Ubuntu/Debian participants run it in their normal Bash terminal. The script installs the base packages, k9s, kubectl, Helm, kubelogin, Krew, and the `oidc-login` plugin, then verifies them.

```bash
set -euo pipefail

case "$(uname -m)" in
  x86_64) TOOL_ARCH="amd64" ;;
  aarch64|arm64) TOOL_ARCH="arm64" ;;
  *) echo "Unsupported CPU architecture: $(uname -m)" >&2; exit 1 ;;
esac

sudo apt-get update
sudo apt-get install -y \
  ca-certificates curl git gzip openssl python3 tar unzip \
  libsecret-1-0 gnome-keyring dbus-x11

INSTALL_DIR="$(mktemp -d)"
trap 'rm -rf "$INSTALL_DIR"' EXIT
cd "$INSTALL_DIR"

# k9s
K9S_VERSION="$(curl -fsSLI -o /dev/null -w '%{url_effective}' \
  https://github.com/derailed/k9s/releases/latest | sed 's#.*/##')"
curl -fsSLO \
  "https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_${TOOL_ARCH}.tar.gz"
tar -xzf "k9s_Linux_${TOOL_ARCH}.tar.gz" k9s
sudo install -m 0755 k9s /usr/local/bin/k9s

# kubectl
KUBECTL_VERSION="$(curl -fsSL https://dl.k8s.io/release/stable.txt)"
curl -fsSLo kubectl \
  "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${TOOL_ARCH}/kubectl"
sudo install -m 0755 kubectl /usr/local/bin/kubectl

# Helm
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 \
  -o get_helm.sh
chmod 700 get_helm.sh
DESIRED_VERSION=v4.2.0 ./get_helm.sh

# kubelogin
curl -fsSLo kubelogin.zip \
  "https://github.com/Azure/kubelogin/releases/latest/download/kubelogin-linux-${TOOL_ARCH}.zip"
unzip -q -o kubelogin.zip
sudo install -m 0755 "bin/linux_${TOOL_ARCH}/kubelogin" /usr/local/bin/kubelogin

# Krew
export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
if ! kubectl krew version >/dev/null 2>&1; then
  KREW_ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')"
  KREW="krew-linux_${KREW_ARCH}"
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz"
  tar -xzf "${KREW}.tar.gz"
  ./"${KREW}" install krew
fi
grep -qxF 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' "$HOME/.bashrc" 2>/dev/null \
  || echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >> "$HOME/.bashrc"

# OIDC login plugin
if kubectl krew list 2>/dev/null | grep -qx 'oidc-login'; then
  kubectl krew upgrade oidc-login
else
  kubectl krew install oidc-login
fi

cd "$HOME"
kubectl version --client
helm version
k9s version
kubelogin --version
kubectl krew version
kubectl oidc-login --help >/dev/null
echo "All Ubuntu/WSL workshop tools installed successfully."
```

> **WSL Helm note:** Installing `libsecret-1-0`, `gnome-keyring`, and `dbus-x11` provides the common credential-store components, but it does not guarantee that every WSL session has an active keyring. If a later Helm OCI command reports a secret-storage error, show the error to the facilitator and run that Helm command in a D-Bus session as described in the troubleshooting note for the deployment step.

### Path B — macOS: Run One Installation Script

Run this entire block in **Terminal on your physical Mac**, not in the browser-based Workbench VSCode terminal. It supports Intel and Apple Silicon Macs, installs Homebrew when necessary, installs the workshop tools, installs Krew using its supported installer, adds Homebrew and Krew to the shell `PATH`, and verifies everything.

```bash
set -euo pipefail

if ! xcode-select -p >/dev/null 2>&1; then
  xcode-select --install
  echo "Finish the Xcode Command Line Tools installation, then run this script again."
  exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

BREW_BIN="$(command -v brew 2>/dev/null || true)"
if [[ -z "$BREW_BIN" ]]; then
  if [[ -x /opt/homebrew/bin/brew ]]; then
    BREW_BIN="/opt/homebrew/bin/brew"
  elif [[ -x /usr/local/bin/brew ]]; then
    BREW_BIN="/usr/local/bin/brew"
  else
    echo "Homebrew was installed but could not be found. Open a new Terminal and run this script again."
    exit 1
  fi
fi

eval "$("$BREW_BIN" shellenv)"
BREW_INIT="eval \"\$(${BREW_BIN} shellenv)\""
touch "$HOME/.zprofile"
grep -qxF "$BREW_INIT" "$HOME/.zprofile" 2>/dev/null \
  || printf '%s\n' "$BREW_INIT" >> "$HOME/.zprofile"

brew update
brew install curl git python kubectl
brew install derailed/k9s/k9s

HELM_INSTALLER="$(mktemp)"
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 \
  -o "$HELM_INSTALLER"
chmod 700 "$HELM_INSTALLER"
DESIRED_VERSION=v4.2.0 "$HELM_INSTALLER"
rm -f "$HELM_INSTALLER"

export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
if ! kubectl krew version >/dev/null 2>&1; then
  (
    set -e
    cd "$(mktemp -d)"
    KREW_OS="$(uname | tr '[:upper:]' '[:lower:]')"
    KREW_ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')"
    KREW="krew-${KREW_OS}_${KREW_ARCH}"
    curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz"
    tar -xzf "${KREW}.tar.gz"
    ./"${KREW}" install krew
  )
fi
grep -qxF 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' "$HOME/.zshrc" 2>/dev/null \
  || echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >> "$HOME/.zshrc"

if kubectl krew list 2>/dev/null | grep -qx 'oidc-login'; then
  kubectl krew upgrade oidc-login
else
  kubectl krew install oidc-login
fi

kubectl version --client
helm version
k9s version
python3 --version
kubectl krew version
kubectl oidc-login --help >/dev/null
echo "All macOS workshop tools installed successfully."
```

This workshop uses the generic OIDC plugin exposed as `kubectl oidc-login`. Krew installs that plugin directly, so do not install the separate Azure `kubelogin` formula for this workshop.

When your selected script prints its success message, continue to Step 1B.

---

## Step 1B: Connect Your Terminal to the Workshop Cluster

Your facilitator will provide a **kubeconfig file** - a credential file that lets your terminal communicate with the cluster.

Save the kubeconfig content to your machine:

Create the kubeconfig file with the following content:

```bash
mkdir -p ~/.kube
cat > ~/.kube/kube_config_aai.yaml << 'EOF'
apiVersion: v1
clusters:
- cluster:
    insecure-skip-tls-verify: true
    server: https://k8s.amd-workshop.silogen.ai
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      args:
      - oidc-login
      - get-token
      - --oidc-issuer-url=https://kc.amd-workshop.silogen.ai/realms/airm
      - --oidc-client-id=k8s
      - --oidc-client-secret=<provided-oidc-client-secret>
      - --insecure-skip-tls-verify
      command: kubectl
      env: null
      interactiveMode: IfAvailable
      provideClusterInfo: false
EOF
```

Activate the kubeconfig:

```bash
export KUBECONFIG=~/.kube/kube_config_aai.yaml
```

The OIDC login will trigger your browser.

Set your namespace. Replace `N` with your assigned participant number; if the facilitator provided a different project name, use that name instead:

```bash
namespace="projN"   # For example, user1 normally uses proj1
```

Trigger the browser login and verify that your account can access its namespace:

```bash
kubectl auth can-i get pods -n "$namespace"
```

When the browser opens, sign in as `userN@amd-workshop.silogen.ai` (for example, `user1@amd-workshop.silogen.ai`) and use the password provided by the workshop facilitator. A successful participant login should return `yes` for the namespace access check.

> **Note:** `kubectl get nodes` requires administrator permissions and is not a participant connectivity test.

---

## Step 1C: Understand How AIMs Deploy Under the Hood

For this CLI exercise, you will deploy the AIM container directly with a native Kubernetes `Deployment`, then expose it with a Kubernetes `Service`. The model container serves an OpenAI-compatible API on port `8000`.

The deployment does **not** put a Hugging Face token in the YAML. Instead, it reads `HF_TOKEN` from a Kubernetes Secret named `hf-token` in your namespace.
<!--
Verify the workshop Secret exists:

```bash
kubectl get secret hf-token -n $namespace
```

The workshop cluster should provide this Secret ahead of time with a key named `token`. You can verify the key name without printing the token value:

```bash
kubectl get secret hf-token -n $namespace -o yaml \
  | sed -n '/^data:/,/^[^ ]/p' \
  | sed -n 's/^  \([^:]*\):.*/key: \1/p'
```

Expected output:

```text
key: token
```
this doesn't work! get error can't get secret-->
<!--
> **Facilitator setup:** For a public workshop, do not publish the Hugging Face token in this guide. Pre-create `hf-token` in every participant namespace with key `token`, or use External Secrets Operator / your platform secret manager to sync the same secret into each namespace. If a cluster uses a different key name, update the `secretKeyRef.key` field in the deployment YAML to match.

TODO facilitator add hf-token to all project namespaces as kubernetes secrets -->

> **Note:** Hugging Face tokens have been pre-loaded into your project namespace for this workshop. As a regular project user you do not have permission to view or modify secrets directly — this is by design. In a real deployment, a platform administrator would manage them through Kubernetes or an external secret manager.

---

## Step 1D: Deploy an AIM via kubectl

Create the deployment manifest:

```bash
cat <<'EOF' > aai-test-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: minimal-aim-deployment
  labels:
    app: minimal-aim-deployment
spec:
  progressDeadlineSeconds: 3600
  replicas: 1
  selector:
    matchLabels:
      app: minimal-aim-deployment
  template:
    metadata:
      labels:
        app: minimal-aim-deployment
    spec:
      containers:
        - name: minimal-aim-deployment
          image: amdenterpriseai/aim-meta-llama-llama-3-2-1b-instruct:0.11.1
          imagePullPolicy: Always
          env:
            - name: AIM_PRECISION
              value: "FP16"
            - name: AIM_GPU_COUNT
              value: "1"
            - name: AIM_GPU_MODEL
              value: "MI350X"
            - name: AIM_ENGINE
              value: "vllm"
            - name: AIM_METRIC
              value: "latency"
            - name: AIM_LOG_LEVEL_ROOT
              value: "INFO"
            - name: AIM_LOG_LEVEL
              value: "INFO"
            - name: AIM_PORT
              value: "8000"
            - name: HF_TOKEN
              valueFrom:
                secretKeyRef:
                  name: hf-token
                  key: token
          ports:
            - name: http
              containerPort: 8000
          resources:
            requests:
              memory: "16Gi"
              cpu: "4"
              amd.com/gpu: "1"
            limits:
              memory: "16Gi"
              cpu: "4"
              amd.com/gpu: "1"
          startupProbe:
            httpGet:
              path: /v1/models
              port: http
            periodSeconds: 10
            failureThreshold: 360
          livenessProbe:
            httpGet:
              path: /health
              port: http
          readinessProbe:
            httpGet:
              path: /v1/models
              port: http
          volumeMounts:
            - name: ephemeral-storage
              mountPath: /tmp
            - name: dshm
              mountPath: /dev/shm
      volumes:
        - name: ephemeral-storage
          emptyDir:
            sizeLimit: 256Gi
        - name: dshm
          emptyDir:
            medium: Memory
            sizeLimit: 32Gi
EOF
```

Create the service manifest:

```bash
cat <<'EOF' > aai-test-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: minimal-aim-deployment
  labels:
    app: minimal-aim-deployment
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      targetPort: 8000
  selector:
    app: minimal-aim-deployment
EOF
```

Apply both manifests to your namespace:

```bash
kubectl apply -f aai-test-deployment.yaml -f aai-test-service.yaml -n $namespace
```

> **Why Llama 3.2 1B?** This AIM image is packaged and optimized for AMD Instinct GPUs. It can take several minutes to download model weights, compile kernels, and pass its startup probe on first launch.

Watch the AIM come up:

```bash
kubectl rollout status deployment/minimal-aim-deployment -n $namespace --timeout=15m
kubectl get pods -n $namespace -l app=minimal-aim-deployment
```

You can also watch it in k9s:

```bash
k9s -n $namespace
```

Wait until the AIM pod shows **Running** and **1/1 Ready** before continuing to Part 2.

If the pod reports `CreateContainerConfigError`, check the Secret key:

```bash
kubectl describe pod -n $namespace -l app=minimal-aim-deployment
```

If the event says `couldn't find key ... in Secret`, update `secretKeyRef.key` in `aai-test-deployment.yaml` to match the key shown by the Secret verification command, then re-apply the deployment.

---

## Step 1E: Query the AIM Directly

Once the pod is **Running**, confirm the model is serving by sending a test request.

Port-forward the service:

```bash
kubectl port-forward service/minimal-aim-deployment 8000:80 -n $namespace
```

In a second terminal, verify the model endpoint:

```bash
curl http://localhost:8000/v1/models
```

Then send a test inference request:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.2-1B-Instruct",
    "messages": [{"role": "user", "content": "Summarize the key benefits of AMD MI350X GPUs in two sentences."}],
    "max_tokens": 150
  }'
```

The response streams back in OpenAI-compatible format, meaning any application already written for OpenAI's API can point to this endpoint with no code changes.
<!-- this doesn't work for user...kubectl get nodes and svc don't work
Now note the AIM's internal service name. You will use it in Step 2B:

```bash
kubectl get svc minimal-aim-deployment -n $namespace
```
-->

Set the service name as a variable:

```bash
aimservice="minimal-aim-deployment"
```

---
## CLI Deployment Patterns

| Scenario | Recommended approach |
|---|---|
| Automated deployment from CI/CD | **kubectl / AIM Engine CLI** |
| GitOps — model config stored in git | **kubectl apply** with YAML manifests |
| Batch deployment of many models | **kubectl** with a loop or Helm |

---

# Module 2 — Part 2: Solution Blueprints — Deploy and Customize a Medical Imaging AI Application (20 minutes)

## Why Solution Blueprints?

Building an AI application from scratch — even with a model already running — still requires writing a UI, a backend, prompt engineering, API wiring, and deployment code. For enterprise teams evaluating use cases, this delay kills momentum.

**Solution Blueprints** eliminate that gap. Each Blueprint is a complete, production-ready AI application distributed as a single deployable package. In this section you will deploy the **MRI Documentation Blueprint** — a full application for AI-assisted medical imaging analysis and report generation — connected directly to the AIM you deployed in Part 1.

---

## Step 2A: Deploy the MRI Documentation Blueprint

The commands in this section follow the upstream [MRI Analysis Tool Deployment Guide](https://github.com/amd-enterprise-ai/solution-blueprints/blob/main/solution-blueprints/mri-doc/docs/DEPLOYMENT.md).

The **MRI Documentation Blueprint** (`aimsb-mri-doc`) provides:
- AI-assisted analysis and summarization of MRI scan reports
- Natural language querying over medical imaging documentation
- Automated report generation for radiologists and clinical teams
- A ready-to-use web interface for healthcare and imaging workflows

### Set Your Variables

```bash
name="my-deployment"       # A unique label for your Blueprint deployment
chart="aimsb-mri-doc"      # The MRI Documentation Blueprint
```

### Deploy

Deploy the Blueprint pointed at the AIM you deployed in Part 1, by listing it as the existing AIMS service:

```bash
helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  --set llm.existingService=$aimservice \
  --set http_route.enabled=true \
  | kubectl apply -f - -n $namespace
```

This follows the Blueprint deployment guide's recommended pattern: render with `helm template`, then pipe the manifests to `kubectl apply`. The chart creates a namespaced `HTTPRoute` when `http_route.enabled=true`.

> **HTTPS prerequisite:** A Gateway named `https` must exist in the `envoy-gateway-system` namespace and have a configured listener. The workshop platform provides this shared Gateway.

> **Helm compatibility:** The upstream guide documents a known stdout issue in Helm 4.2.1 and newer that can break `helm template ... | kubectl apply -f -`. Both Step 1A installation scripts pin Helm 4.2.0. If you use another workstation, use Helm 3.16 through 4.2.0 or follow the upstream guide's separate `helm pull --untar` workaround.

### Verify the Deployment

```bash
k9s -n $namespace
```

This opens a live dashboard scoped to your namespace. Pods will initially show `ContainerCreating` or `Pending` while images pull — this is normal. Watch the **STATUS** column until all pods show **Running** before continuing. Press `:q` to exit k9s.

> **k9s tips:** Use the arrow keys to navigate between pods. Press `d` to describe a pod (useful for troubleshooting), `l` to stream its logs, and `:q` to exit.

![Blueprint deployment in progress](aai_workshop_images/blueprint-wsl-deployment.png)

Confirm that Kubernetes accepted the HTTPS route and resolved its service reference:

```bash
kubectl get httproute aimsb-mri-doc-$name -n $namespace
kubectl describe httproute aimsb-mri-doc-$name -n $namespace
```

In the `Status` section, look for `Accepted=True` and `ResolvedRefs=True`. If either condition is false, show the `kubectl describe` output to the facilitator before continuing.

### Access the MRI Documentation Application via HTTPS

Once the deployment and route are ready, print the application URL:

```bash
blueprint_url="https://aimsb-mri-doc-$name$(kubectl get gtw -A -o jsonpath='{.items[*].spec.listeners[?(@.name=="https")].hostname}' | tr -d \*)/"
echo "$blueprint_url"
```

This command follows the Blueprint deployment guide by querying the cluster for the `https` listener hostname instead of hard-coding a domain. The Gateway terminates TLS and routes the resulting hostname to the Blueprint service. No local port-forward is required.

Verify HTTPS from the terminal:

```bash
curl --fail --show-error --location "$blueprint_url"
```

Open the printed URL in your browser. You should see the MRI Documentation interface. Try uploading a sample MRI report or asking it a question about an imaging study.

> **What does this do?**
> - `helm template` downloads the Blueprint chart from AMD's registry and renders it into Kubernetes configuration files
> - `--set llm.existingService=$aimservice` points the Blueprint at the Llama 3.2 1B AIM service you deployed in Part 1 — no second model pod is created
> - `--set http_route.enabled=true` creates the `HTTPRoute` using the chart's Gateway configuration
> - `kubectl apply` sends the rendered configuration to the cluster






---

## Step 2B: Blueprint Customization

Blueprints are open-source — the source code is available on GitHub and every component can be modified. In this section you will tear down the current Blueprint deployment and redeploy it with a different configuration to see how easy customization is.

**1. Tear Down and Redeploy with a Default AIM**

Delete the existing Blueprint and its HTTPS route:

```bash
helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  --set llm.existingService=$aimservice \
  --set http_route.enabled=true \
  | kubectl delete -f - -n $namespace
```

Wait for pods to terminate (watch in k9s), then redeploy the Blueprint — this time pointing it to the default AIMs in the helmchart (GPT-OSS-20B):

```bash
helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  --set http_route.enabled=true \
  | kubectl apply -f - -n $namespace
```

Wait for the pods to restart, then confirm the route is accepted:

```bash
kubectl get httproute aimsb-mri-doc-$name -n $namespace
curl --fail --show-error --location "$blueprint_url"
```

Open `$blueprint_url` in your browser. The Blueprint is now powered by the AIM included by the chart instead of the shared AIM from Part 1.

> **Why does this matter?** Running a separate model per application wastes GPU resources and creates management complexity. By pointing Blueprints at a shared AIM, your team gets one model to monitor, update, and scale — and every application benefits automatically. This is also how you would swap in a different model without rebuilding the Blueprint.

**2. Change the System Prompt**

Each Blueprint exposes prompt configuration. Edit the system prompt to adapt the AI's output style — for example, switching from radiologist-facing technical language to patient-friendly plain-English summaries, or restricting responses to a specific imaging modality (MRI, CT, X-ray).

**3. Upgrade the Image Segmentation Model (UNet via MONAI) *(optional)***

The Blueprint currently segments brain tissue using simple K-means clustering inside `segment_brain_tissue()` in `src/mri_analysis.py`. You can replace this with a deep learning UNet model from a [MONAI bundle](https://monai.io/model-zoo.html) for clinical-grade accuracy — identifying tumor boundaries, organ contours, and tissue types with far greater precision.

First, clone the Blueprint source:

```bash
git clone https://github.com/amd-enterprise-ai/solution-blueprints.git
cd solution-blueprints/solution-blueprints/mri-doc
```

**Step 1 — Add dependencies to `src/requirements.txt`**

The Blueprint installs Python packages fresh on every pod start from `src/requirements.txt` (there is no pre-built container image — code is embedded in a Kubernetes ConfigMap via Helm). Add `monai` and `torch` before deploying:

```
monai
torch
```

> **Note:** PyTorch is several GB. The first pod startup after this change will take 5–15 minutes while packages are downloaded and installed inside the container.

**Step 2 — Edit `src/mri_analysis.py`**

Open `src/mri_analysis.py` and find the `segment_brain_tissue()` method inside the `MRIProcessor` class. The current K-means implementation looks like this:

```python
# Current: simple K-means clustering (class method inside MRIProcessor)
def segment_brain_tissue(self, image):
    """Segment tissue using K-means clustering."""
    if image is None:
        return None, {}

    from sklearn.cluster import KMeans

    pixels = image.reshape((-1, 1))
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels)
    segmented = labels.reshape(image.shape)

    unique, counts = np.unique(labels, return_counts=True)
    total_pixels = len(pixels)

    tissue_stats = {}
    for cluster, count in zip(unique, counts):
        percentage = (count / total_pixels) * 100
        tissue_stats[f"Tissue_Cluster_{cluster}"] = {"pixel_count": int(count), "percentage": round(percentage, 2)}

    return segmented, tissue_stats
```

Replace it with a MONAI UNet inference call. The method must remain a class method with the same signature and return the same `(segmented, tissue_stats)` tuple so the rest of the class continues to work:

```python
# Upgraded: MONAI UNet from a pretrained bundle (class method inside MRIProcessor)
def segment_brain_tissue(self, image, model_path="/tmp/brain_segmentation_unet.pth"):
    import torch
    from monai.networks.nets import UNet
    from monai.transforms import Compose, EnsureChannelFirst, ScaleIntensity, ToTensor

    if image is None:
        return None, {}

    # Load pretrained UNet
    model = UNet(
        spatial_dims=2,
        in_channels=1,
        out_channels=3,       # 3 tissue classes: CSF, grey matter, white matter
        channels=(16, 32, 64, 128),
        strides=(2, 2, 2),
    )
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    # channel_dim="no_channel" is required for plain 2D numpy arrays (MONAI 1.x)
    transform = Compose([EnsureChannelFirst(channel_dim="no_channel"), ScaleIntensity(), ToTensor()])
    input_tensor = transform(image).unsqueeze(0)   # add batch dim → (1, 1, H, W)

    with torch.no_grad():
        output = model(input_tensor)
    labels = output.argmax(dim=1).squeeze().numpy()
    segmented = labels.astype(np.float32) / 2          # normalise to [0, 1] for 3 classes

    # Return tissue_stats in the same format as the K-means implementation
    unique, counts = np.unique(labels, return_counts=True)
    total_pixels = labels.size
    tissue_stats = {}
    for cluster, count in zip(unique, counts):
        percentage = (count / total_pixels) * 100
        tissue_stats[f"Tissue_Cluster_{int(cluster)}"] = {
            "pixel_count": int(count),
            "percentage": round(float(percentage), 2),
        }

    return segmented, tissue_stats
```

**Step 3 — Download and stage the model weights**

Download a pretrained brain segmentation bundle from the MONAI Model Zoo. Run this on your local machine (outside the pod) before copying the weights in:

```bash
# Download the pretrained bundle weights locally
python3 -c "
from monai.bundle import download
download('brain_image_segmentation', bundle_dir='/tmp/monai_bundle')
"
# Find the downloaded .pt/.pth weights file
find /tmp/monai_bundle -name "*.pt" -o -name "*.pth"
```

> **Note:** The bundle download path and filename will depend on the bundle version. Use the path printed by the `find` command in the `kubectl cp` step below.

The pod uses ephemeral storage, so copy the weights into the running pod directly:

```bash
# Find the pod name
kubectl get pods -n $namespace -l app=aimsb-mri-doc-$name

# Copy weights into the pod (replace <weights-file> with the path from the find command above)
kubectl cp /tmp/monai_bundle/<weights-file> \
  $namespace/<pod-name>:/tmp/brain_segmentation_unet.pth
```

> **Note:** Weights copied this way are lost on pod restart. For a durable setup, pre-seed a PersistentVolumeClaim or download the weights inside a startup script in `values.yaml`.

**Step 4 — Redeploy via Helm**

There is no container image to build — the Blueprint packages `src/*.py` and `src/requirements.txt` directly into a ConfigMap. Confirm you are still in the `mri-doc` directory, then follow the deployment guide's `helm template | kubectl apply` pattern to push your changes:

```bash
# Confirm you are in the right directory
pwd   # should end with solution-blueprints/mri-doc

helm template $name . \
  --set llm.existingService=$aimservice \
  --set http_route.enabled=true \
  -f values.yaml \
  | kubectl apply -f - -n $namespace
```

The pod will restart, install the updated dependencies, and mount the new code. The application will now use deep learning segmentation on every uploaded scan.

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

## Cleanup: Undeploy the AIM

If your Blueprint is still configured to use `minimal-aim-deployment`, undeploy or redeploy the Blueprint first. Deleting the AIM while an app depends on it will leave the app without a model backend.

Stop any active port-forward with `Ctrl+C`, then delete the AIM deployment and service:

```bash
kubectl delete -f aai-test-deployment.yaml -f aai-test-service.yaml -n $namespace
```

If you no longer have the YAML files, delete the resources by name:

```bash
kubectl delete deployment/minimal-aim-deployment service/minimal-aim-deployment \
  -n $namespace \
  --ignore-not-found
```

Verify the AIM resources are gone:

```bash
kubectl get deploy,svc,pods -n $namespace -l app=minimal-aim-deployment
```

Leave the `hf-token` Secret in place. It is a namespace-level workshop credential and may be reused by other AIM deployments.

---

## Taiwan ODM Workshop Complete

You have now completed the core CLI deployment workflow for AIMs and Solution Blueprints:

| What You Did | What It Demonstrates |
|---|---|
| Deployed an AIM via kubectl | Programmable, CLI-native model lifecycle management |
| Deployed a Solution Blueprint pointed at your AIM | Complete AI applications in minutes, no redundant model deployment |
| Tore down and redeployed the Blueprint with a different configuration | Open-source, composable applications that share a single model |

**Next steps:**
- Explore additional Solution Blueprints at [AMD Enterprise AI](https://enterprise-ai.docs.amd.com)
- Ask your facilitator about bringing the AMD AI platform to your organization
- Review the [AMD Enterprise AI documentation](https://enterprise-ai.docs.amd.com) for architecture guides and API references
