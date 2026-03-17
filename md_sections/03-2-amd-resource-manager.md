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

