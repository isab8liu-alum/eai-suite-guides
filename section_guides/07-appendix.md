# Appendix

------------------------------------------------------------------------

## Useful Commands

### Check Running Pods

List all pods across all namespaces and their current status:

```bash
kubectl get pods -A
```

or use k9s if installed

Use this to verify workloads are running or to identify pods in an error state.

### Check Services and Endpoints

List all services across all namespaces, including their cluster IPs and ports:

```bash
kubectl get svc -A
```

Use this to find the service name of a running AIM deployment (needed for Blueprint configuration).

### Inspect a Pod

Get detailed information about a specific pod, including events that may explain why it is not starting:

```bash
kubectl describe pod <pod-name> -n <namespace>
```

### View Pod Logs

Stream the logs from a running or failed pod:

```bash
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous   # Logs from a previously crashed container
```

### Get Your Namespace Name

```bash
kubectl get namespaces
```

------------------------------------------------------------------------

## Glossary

| Term | Definition |
|------|------------|
| **AIM** | AI Model — a packaged, optimized inference model available in the AMD AI Workbench catalog |
| **Blueprint** | A reference solution application built on one or more AIMs, distributed as a Helm chart |
| **Cluster Bloom** | The installation tool that sets up the Kubernetes cluster and deploys the EAI Suite |
| **EAI Suite** | AMD Enterprise AI Suite — the full platform including Resource Manager, AI Workbench, and supporting services |
| **Helm** | A package manager for Kubernetes that deploys applications defined in reusable "charts" |
| **Keycloak** | The identity and access management service used by EAI Suite for authentication |
| **kubectl** | The Kubernetes command-line tool used to interact with the cluster |
| **nip.io** | A public DNS service that automatically resolves hostnames containing an IP address (e.g., `app.1.2.3.4.nip.io` resolves to `1.2.3.4`) |
| **Quota** | A guaranteed resource allocation (GPUs, CPU, memory) assigned to a project |
| **ROCm** | AMD's open-source software platform for GPU-accelerated computing |
| **Workload** | A running job in the platform — e.g., a deployed model inference service or a finetuning job |
| **Workspace** | A pre-configured development environment (e.g., VSCode, JupyterLab) accessible via the browser |

------------------------------------------------------------------------

## Reference Documentation

- [EAI Suite Documentation](https://enterprise-ai.docs.amd.com/en/latest/)
- [Solution Blueprints Overview](https://enterprise-ai.docs.amd.com/en/latest/solution-blueprints/overview.html)
- [On-Premises Installation Guide](https://enterprise-ai.docs.amd.com/en/latest/platform-infrastructure/on-premises-installation.html)
- [Accessing the Cluster (kubeconfig)](https://enterprise-ai.docs.amd.com/en/latest/resource-manager/workloads/accessing-the-cluster.html)
- [Hugging Face Token Settings](https://huggingface.co/settings/tokens)

------------------------------------------------------------------------

**Maintained by AMD — Internal Documentation**
