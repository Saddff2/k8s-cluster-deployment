# Kubernetes Cluster Deployment 

This guide will explore a method for deploying and managing your **Kubernetes** cluster.   
Specifically, we will focus on building our infrastructure around a **Flask** application connected to **MongoDB** as our main application.  
We will use **ArgoCD** for automatic deployment of our **Helm Charts** and **Docker Images**, **Jenkins** and **GitLab** **CI** for **CI/CD** pipelines and **Grafana** + **Prometheus** stack for monitoring. 

## Contents


### Prerequisites
I'm using  **Google Kubernetes Engine** (GKE) from Google Cloud Platform (GCP) as a provider for my cluster.  
You also can use local clusters such as **Minikube**, **Kind**, or **Docker Desktop Kubernetes Engine**.  
Our you can use **Terraform** and **[Kubespray](https://github.com/kubernetes-sigs/kubespray)** and deploy your cluster pretty easy on baremetal or any cloud.

## Overview of the Infrastucture

<img src="images/Screenshot_2024-07-02_at_20.27.45.png" width="900">

####  ArgoCD

Continuing with our setup, we will leverage the capabilities of ArgoCD for continuous deployment and GitOps practices. ArgoCD will automate the deployment of our Helm Charts and Docker images, ensuring that our infrastructure stays in sync with our desired state defined in Git repositories.

It will continuously monitor our GitLab Repository for changes and sync them immediatly after changes. It will not only monitor changes to our Flask Application, but also to Jenkins, Grafana + Prometheus, and ArgoCD itself.

#### Jenkins / Gitlab CI

For our CI/CD pipelines, Jenkins and GitLab CI will play crucial roles in automating our build, test, and deployment processes.

* Jenkins: We’ll configure Jenkins to handle our CI/CD workflows. It will integrate seamlessly with our Git repositories. Jenkins pipelines will build our Docker images, run tests, and deploy updates to Kubernetes using Helm charts managed by ArgoCD.
* GitLab CI: GitLab CI will complement Jenkins by providing additional pipelines that manage specific aspects of our development lifecycle. It will monitor changes in our GitLab repositories and trigger pipelines accordingly, ensuring robust automation from code commit to deployment.

#### Grafana + Prometheus

The Grafana + Prometheus stack will provide comprehensive monitoring and observability for our Kubernetes cluster and applications.

* Prometheus: Prometheus will collect metrics from Kubernetes components, including pods, nodes, and services. It will also scrape metrics from our Flask application and MongoDB instances. Prometheus supports flexible querying, allowing us to create custom alerts based on metrics thresholds and trends. This ensures proactive monitoring and alerting for any anomalies or performance issues within our infrastructure.
* Grafana: Grafana will visualize Prometheus metrics through customizable dashboards. We can create specific dashboards to monitor the health and performance of our Flask application, MongoDB databases, Kubernetes cluster utilization, Jenkins/GitLab CI pipelines, and ArgoCD deployments. Grafana’s rich visualization capabilities enable us to gain insights into key metrics, track trends over time, and troubleshoot issues efficiently.

### Explanation of the Workflow
