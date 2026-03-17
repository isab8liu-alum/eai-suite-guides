# 5. Troubleshooting

Common issues you may encounter during the lab and how to resolve them.

------------------------------------------------------------------------

## Login / Authentication Issues

**Symptom:** Cannot log in to the AMD Resource Manager or Workbench UI.

- Verify you are using the correct URL format: `https://airmui.<your-ip>.nip.io`
- Verify your username includes the domain: `devuser@<your-ip>.nip.io`
- Default password is `password` — if you changed it and forgot it, contact your lab instructor
- Ensure the IP address in your URL matches the droplet IP assigned to you

------------------------------------------------------------------------

## Project Quota Errors

**Symptom:** Workload fails to start with a quota or resource error.

- Navigate to **Resource Manager → Projects → [your project] → Quota** and confirm GPUs and memory are set to non-zero values
- Confirm you clicked **Save changes** after setting quotas
- Check that no other workload in the same project is consuming the full quota

------------------------------------------------------------------------

## `minio-credentials-fetcher` Not in Secrets Dropdown

**Symptom:** The `minio-credentials-fetcher` secret does not appear when assigning a storage secret to a project.

- This secret is created during platform installation. If it is missing, the installation may not have completed successfully.
- <!-- TODO: Add resolution steps, e.g., how to verify minio is running or reinstall the secret -->
- Contact your lab instructor if the secret is not available.

------------------------------------------------------------------------

## Model Deployment Stuck in Pending

**Symptom:** A deployed model shows `Pending` status in the Workloads view and does not transition to `Running`.

- Wait up to 5 minutes — the first deployment pulls a container image and may take longer than expected
- Check GPU quota: navigate to **Projects → Quota** and confirm GPU quota is set and saved
- Check pod events for details:
  ```bash
  kubectl get pods -n <your-namespace>
  kubectl describe pod <pod-name> -n <your-namespace>
  ```
- Look for `Insufficient nvidia.com/gpu` or similar resource errors in the pod events output

------------------------------------------------------------------------

## Hugging Face Token Errors (Gated Models)

**Symptom:** Model deployment fails with an authentication or access error for gated models (e.g., Llama).

- Verify your Hugging Face token has access to the model. Check at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Ensure you accepted the model's license agreement on the Hugging Face model page
- Re-enter the token in the deployment dialog — tokens are not validated until the deployment starts

------------------------------------------------------------------------

## VSCode Workspace Fails to Launch

**Symptom:** Clicking "Launch" on the VSCode workspace does nothing, or the page fails to load.

- Verify the workspace shows a `Running` status in the Workloads view before clicking Launch
- Try refreshing the Workspaces page and launching again
- <!-- TODO: Add any environment-specific notes, e.g., browser compatibility or port forwarding requirements -->

------------------------------------------------------------------------

## Helm / kubectl Not Found

**Symptom:** `helm: command not found` or `kubectl: command not found` in the terminal.

- If using the VSCode workspace terminal, these tools may need to be installed or the terminal session may need to be refreshed
- <!-- TODO: Add installation instructions or confirm whether these tools are pre-installed in the HOL environment -->
- Verify with: `which helm` and `which kubectl`

------------------------------------------------------------------------

## Cluster Bloom Configuration Failed or Timed Out

> **Note:** This section applies to environment setup only. During the HOL, the environment is pre-installed and this should not occur. Contact your lab instructor if you believe there is an environment issue.

If the installation must be re-run, try:

```bash
sudo ./bloom cli --config bloom.yaml
```

If the issue persists:

- Verify disk mapping (`/dev/vdc1`) is correct for your environment
- Ensure the droplet has sufficient resources
- Confirm network access is not blocked

------------------------------------------------------------------------
