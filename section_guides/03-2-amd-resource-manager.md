# 2. AMD Resource Manager

## Overview

AMD Resource Manager provides platform administrators with tools to oversee and control the platform's computational resources and user access. Key capabilities include cluster management, monitoring, and maintaining teams' access to computational resources.

![AMD Resource Manager Dashboard](../images/03-resource-manager/01-dashboard-overview.png)

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

1. From the **Dashboard**, click **Projects** in the left sidebar
2. Click the **Create project** button
3. Enter a project name, an optional description, and select your cluster
4. Click **Create project**

![Projects page with Create project button](../images/03-resource-manager/02-projects-page.png)

![Create project dialog with fields filled in](../images/03-resource-manager/04-create-project-filled.png)

> **Expected outcome:** You are redirected to the **Project settings** page for your new project.

------------------------------------------------------------------------

### Step 2 — Adjusting Quota

You should now be on the **Project settings** page with the **Quota** tab active. Quotas ensure fair and shared resource allocation across projects.

Set the resource allocation for your project:

1. **GPUs** — Number of GPU devices
2. **CPU Cores** — Number of CPU cores
3. **System Memory** — Memory allocation in GiB
4. **Ephemeral Disk** — Temporary disk space for workloads
5. Click **Save changes**

<!-- TODO: Add recommended quota values for this HOL exercise, e.g., "For this lab, set GPUs = 1, CPU Cores = 8, Memory = 32 GiB" -->

![Quota tab with resource values set](../images/03-resource-manager/05-quota-tab.png)

> **Expected outcome:** A confirmation message appears and your quota settings are saved.

------------------------------------------------------------------------

### Step 3 — Attaching Storage

Each project requires a storage configuration to download models and run workloads. During installation, a `minio-credentials-fetcher` secret and a default storage configuration are created automatically. You will assign these to your project now.

1. Click the **Secrets** tab
2. Click **Add project secret** and select **Assign existing secret**
3. Select **minio-credentials-fetcher** from the **Secret** drop-down menu
4. Click **Assign secret**

![Secrets tab showing Add project secret button and options](../images/03-resource-manager/06-secrets-tab-add-menu.png)

![Assign secret dialog with minio-credentials-fetcher selected](../images/03-resource-manager/07-assign-secret-minio.png)

![Secrets tab confirming minio-credentials-fetcher assigned](../images/03-resource-manager/08-secret-assigned.png)

> **Expected outcome:** The `minio-credentials-fetcher` secret appears in the project's secrets list.

> **Troubleshooting:** If `minio-credentials-fetcher` does not appear in the drop-down, the platform installation may not have completed successfully. See the [Troubleshooting](./06-5-troubleshooting.md) section.

------------------------------------------------------------------------

### Step 4 — Adding Users to the Project

Users must be added to a project before they can access its resources and run workloads.

1. Click the **Users** tab
2. Click the **Add Member** button
3. Select yourself (and any other desired users) from the **Users** drop-down menu
4. Click **Add to project**

![Users tab showing Add Member button](../images/03-resource-manager/09-users-tab.png)

![Add member dialog with user selected](../images/03-resource-manager/10-add-member-dialog.png)

![Users tab confirming member added](../images/03-resource-manager/11-member-added.png)

> **Expected outcome:** The selected user(s) appear in the project's member list. Your project is now configured and ready to use.

------------------------------------------------------------------------

**Next:** Proceed to [AMD Workbench](./04-3-amd-workbench.md) to deploy a model.
