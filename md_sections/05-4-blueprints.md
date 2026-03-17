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

