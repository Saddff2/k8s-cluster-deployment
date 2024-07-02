# Kubernetes Cluster Deployment 

This guide will explore a method for deploying and managing your **Kubernetes** cluster.   
Specifically, we will focus on building our infrastructure around a **Flask** application connected to **MongoDB** as our main application.  
We will use **ArgoCD** for automatic deployment of our **Helm Charts** and **Docker Images**,  
**Jenkins** and **GitLab** **CI** for **CI/CD** pipelines and **Grafana** + **Prometheus** stack for monitoring. 

## Contents


## Prerequisites
I'm using  **Google Kubernetes Engine** (GKE) from Google Cloud Platform (GCP) as a provider for my cluster.  
You also can use local clusters such as **Minikube**, **Kind**, or **Docker Desktop Kubernetes Engine**.  
Our you can use **Terraform** and **[Kubespray](https://github.com/kubernetes-sigs/kubespray)**  and deploy your cluster pretty easy on baremetal or any cloud.

## Overview of the Infrastucture

<img src="images/Screenshot_2024-07-02_at_20.27.45.png" width="900">

###  ArgoCD

Continuing with our setup, we will leverage the capabilities of ArgoCD for continuous deployment and GitOps practices.  
ArgoCD will automate the deployment of our Helm Charts and Docker images, ensuring that our infrastructure stays in sync with our desired state defined in Git repositories.
It will continuously monitor our GitLab Repository for changes and sync them immediatly after changes.  
It will not only monitor changes to our Flask Application, but also to Jenkins, Grafana + Prometheus, and ArgoCD itself.

### Jenkins / Gitlab CI

For our CI/CD pipelines, Jenkins and GitLab CI will play crucial roles in automating our build, test, and deployment processes.

* Jenkins: We’ll configure Jenkins to handle our CI/CD workflows. It will integrate seamlessly with our Git repositories.  
Jenkins pipelines will build our Docker images, run tests, and deploy updates to Kubernetes using Helm charts managed by ArgoCD.
* GitLab CI: GitLab CI will complement Jenkins by providing additional pipelines that manage specific aspects of our development lifecycle.  
It will monitor changes in our GitLab repositories and trigger pipelines accordingly, ensuring robust automation from code commit to deployment.

### Grafana + Prometheus

The Grafana + Prometheus stack will provide comprehensive monitoring and observability for our Kubernetes cluster and applications.

* Prometheus: Prometheus will collect metrics from Kubernetes components, including pods,  nodes, and services. It will also scrape metrics from our Flask application and MongoDB instances.  
Prometheus supports flexible querying, allowing us to create custom alerts based on metrics thresholds and trends.  
This ensures proactive monitoring and alerting for any anomalies or performance issues within our infrastructure.
* Grafana: Grafana will visualize Prometheus metrics through customizable dashboards.  
We can create specific dashboards to monitor the health and performance of our Flask application,  MongoDB databases, Kubernetes cluster utilization, Jenkins/GitLab CI pipelines, and ArgoCD deployments.  
Grafana’s rich visualization capabilities enable us to gain insights into key metrics, track trends over time, and troubleshoot issues efficiently.


## Explanation of the Workflow



## Cluster Configuration

1.	**Setting up Kubernetes Cluster**:
* Depending on your preference and environment, choose Google Kubernetes Engine (GKE), Minikube, Kind, Docker Desktop Kubernetes Engine, or use Terraform with Kubespray for deployment on bare metal or any cloud provider.

2. **Install ArgoCD**
* Install ArgoCD on your Kubernetes cluster. ArgoCD will serve as our GitOps continuous deployment tool, automating the deployment of Helm charts and Docker images based on changes to Git repositories.

3. **Configure ArgoCD**
* Setup connection to Git repositories using SSH key. Define repositories, Helm charts, and Docker images that ArgoCD will monitor and synchronize with the desired state.
* Install root application, that serves as the central control point for managing our infrastructure and applications deployed on Kubernetes.  
Its main role is to orchestrate the deployment of other applications defined in Git repositories, ensuring they are automatically deployed and synchronized to their desired state.

4. **Configure Jenkins**  
Helm Chart provided in this guide is set up to install all needed plugins for work. So only things to configure are:  
* Create New Account
* Create credentials for Docker and Gitlab
* Make pipeline that points to Jenkinsfile in Gitlab repository


## Step-by-Step Installation Guide

### Installing ArgoCD

```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

```
**Wait for ArgoCD to install.**

Now, use port-forward to access argocd server.
```
kubectl port-forward svc/argocd-server 9101:80 -n argocd

```
**Getting password**
```
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode ; echo
```
**Go to http://localhost:9101**

Now let's login to ArgoCD GUI  
```
Login: admin  
Password: < given password >
```

Go to Settings > Repositories > Connect Repo 

Add your GitLab ssh private key to every repo.

<img src="images/repos-connected.png" width="1100">

### Root yaml

Apply root yaml that is located in gcp-deploy/argocd/bootstrap

```
kubectl apply -f root.yaml
```

**This will take approximately 5 minutes (for 3 nodes cluster with 2 vcpu and 4 vram) for all applications to start.**

<img src="images/apps-running.png" width="1100">

### Access Grafana
