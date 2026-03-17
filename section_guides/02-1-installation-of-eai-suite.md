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

