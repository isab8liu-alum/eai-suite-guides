# 4. Blueprints

Solution Blueprints are reference applications built with AIMs (AI Models). They offer an easy way to explore AIMs in the context of a complete microservice solution. For developers, Solution Blueprints serve as starting points and example implementations, making it fast and easy to solve real-world problems with ROCm software.

Full documentation: [Solution Blueprints Overview](https://enterprise-ai.docs.amd.com/en/latest/solution-blueprints/overview.html)

------------------------------------------------------------------------

## Prerequisites for This Section

Blueprints are deployed via **Helm**, a package manager for Kubernetes. Before proceeding:

- **Helm** must be installed on your terminal environment. Verify with:

  ```bash
  helm version
  ```

- You must have access to the Kubernetes cluster via `kubectl`. If you have not set up cluster access yet, follow the [Accessing the Cluster guide](https://enterprise-ai.docs.amd.com/en/latest/resource-manager/workloads/accessing-the-cluster.html#constructing-the-kubeconfig-file) to obtain and configure your `kubeconfig` file before continuing.

  Verify cluster access with:

  ```bash
  kubectl get nodes
  ```

  <!-- SCREENSHOT: Terminal showing successful `kubectl get nodes` output -->

> **What is Helm?** Helm is a tool that packages Kubernetes application configurations into reusable "charts." Instead of writing and managing many individual Kubernetes YAML files, you deploy a chart with a single command. AMD Solution Blueprints are distributed as Helm charts via a container registry.

------------------------------------------------------------------------

## Deploying a Blueprint

Solution Blueprints are provided as Helm charts. The recommended approach is to render the chart with `helm template` and pipe the output directly to `kubectl apply`. This avoids Helm managing release state, which simplifies cleanup. We don’t recommend helm install, which by default uses a Secret to keep track of the related resources. Ensure you have access to the cluster trough the terminal. Access guide can be found [here](https://enterprise-ai.docs.amd.com/en/latest/resource-manager/workloads/accessing-the-cluster.html#constructing-the-kubeconfig-file).


Replace the placeholder values before running:

- `name` — a unique name for this deployment (e.g., `my-deployment`)
- `namespace` — the Kubernetes namespace for your project (e.g., `my-namespace`)
- `chart` — the name of the blueprint chart to deploy

| Folder | Chart Name |
| --- | --- |
| agentic-testing | aimsb-agentic-testing |
| agentic-translation | aimsb-agentic-translation |
| autogen-studio | aimsb-autogenstudio |
| code-docs-builder | aimsb-codedocs |
| continuedev-assistant | aimsb-continuedev-assistant |
| document-summarization | aimsb-docsum |
| fsi | aimsb-fsi |
| llm-chat | aimsb-llm-chat |
| llm-router | aimsb-llm-router |
| pdf-to-podcast | aimsb-pdf-to-podcast |
| report-generation-engine | aimsb-report-generation-engine |
| talk-to-your-documents | aimsb-talk-to-your-documents |

A full list of available charts can be found at:
     https://enterprise-ai.docs.amd.com/en/latest/solution-blueprints/overview.html 

```bash
name="my-deployment"
namespace="my-namespace"
chart="aimsb-my-chart"   # TODO: Replace with the actual chart name for this HOL

helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  | kubectl apply -f - -n $namespace
```

<!-- SCREENSHOT: Terminal showing the helm template | kubectl apply command and its output -->

After deploying, verify that the blueprint pods are running:

```bash
kubectl get pods -n $namespace
```

<!-- SCREENSHOT: Terminal showing kubectl get pods output with blueprint pods in "Running" state -->

> **Expected outcome:** All pods for the blueprint show a `Running` status. This may take a few minutes as container images are pulled.

------------------------------------------------------------------------

## Reusing an Existing Model Deployment

By default, the Helm chart deploys its own AI model instance. If you already have a compatible AIM deployed from the [Workbench section](./04-3-amd-workbench.md), you can reuse that deployment to save resources.

To point the blueprint at an existing model, set the `existingService` value to the Kubernetes service name of your running AIM. Use the service name alone if it is in the same namespace, or the full DNS form `<SERVICENAME>.<NAMESPACE>.svc.cluster.local:<PORT>` if it is in a different namespace.

```bash
name="my-deployment"
namespace="my-namespace"
chart="aimsb-my-chart"             # TODO: Replace with actual chart name
servicename="aim-llm-my-model-123456"  # TODO: Replace with your deployed model's service name

helm template $name oci://registry-1.docker.io/amdenterpriseai/$chart \
  --set llm.existingService=$servicename \
  | kubectl apply -f - -n $namespace
```

> **Finding your service name:** Run `kubectl get svc -n $namespace` and look for the service associated with your deployed model.

------------------------------------------------------------------------

**Next:** Proceed to the [Troubleshooting](./06-5-troubleshooting.md) guide if you encounter any issues, or the [Appendix](./07-appendix.md) for reference commands and cleanup steps.
