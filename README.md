# Kubernetes Cluster Deployment 

This guide will explore a method for deploying and managing your **Kubernetes** cluster.   
Specifically, we will focus on building our infrastructure around a **Flask** application connected to **MongoDB** as our main application.  
We will use **ArgoCD** for automatic deployment of our **Helm Charts** and **Docker Images**, **Jenkins** and **GitLab** **CI** for **CI/CD** pipelines and **Grafana** + **Prometheus** stack for monitoring. 

I'm using  **Google Kubernetes Engine** (GKE) from Google Cloud Platform (GCP) as a provider for my cluster.  
You also can use local clusters such as **Minikube**, **Kind**, or **Docker Desktop Kubernetes Engine**.  
Our you can use **Terraform** and **Kubespray** and deploy your cluster pretty easy on baremetal or any cloud.

## Overview of the Infrastucture


