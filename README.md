# Kubernetes Cluster Deployment 

This guide will explore a method for deploying and managing your **Kubernetes** cluster.   
Specifically, we will focus on building our infrastructure around a **Flask** application connected to **MongoDB** as our main application.  
We will use **ArgoCD** for automatic deployment of our **Helm Charts** and **Docker Images**,  
**Jenkins** and **GitLab** **CI** for **CI/CD** pipelines and **Grafana** + **Prometheus** stack for monitoring. 

## Contents
- [Prerequisites](#prerequisites)
- [Overview of the Infrastucture](#overview-of-the-infrastructure)
  - [ArgoCD](#argocd)
  - [Jenkins / Gitlab CI](#jenkins--gitlab-ci)
  - [Grafana + Prometheus](#grafana--prometheus)
- [Explanation of the Workflow](#explanation-of-the-workflow)
  - [Continuous Integration (CI) with Jenkins and GitLab CI](#continuous-integration-ci-with-jenkins-and-gitlab-ci)
    - [Code Commit and Push](#code-commit-and-push)
    - [Build and Test](#build-and-test)
    - [Update Helm Chart](#update-helm-chart)
    - [Push Docker Image](#push-docker-image)
  - [Continuous Deployment (CD) with ArgoCD](#continuous-deployment-cd-with-argocd)
    - [Monitoring and Syncing](#monitoring-and-syncing)
    - [Deployment](#deployment)
- [Cluster Configuration](#cluster-configuration)
  - [Setting up Kubernetes Cluster](#setting-up-kubernetes-cluster)
  - [Install ArgoCD](#install-argocd)
  - [Configure ArgoCD](#configure-argocd)
  - [Configure Jenkins](#configure-jenkins)
- [Step-by-Step Installation Guide](#step-by-step-installation-guide)
  - [Installing ArgoCD](#installing-argocd)
  - [Access Grafana](#access-grafana)
  - [Configure Jenkins Pipeline](#configure-jenkins-pipeline)
- [Conclusion](#conclusion)
- [Final Result](#final-result)
- [Additional Resources](#additional-resources)
- [Next Steps](#next-steps)
  - [Ingress Configuration](#ingress-configuration)
  - [Security and Scalability](#security-and-scalability)
  - [Terraform and Kubespray](#terraform-and-kubespray)
- [Thank You](#thank-you)


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


# Explanation of the Workflow

## Continuous Integration (CI) with Jenkins and GitLab CI
### Code Commit and Push

* Developer Commits Code: A developer commits code changes to the GitLab repository.
* GitLab CI Triggers: GitLab CI detects the code commit and triggers the CI pipeline.

### Build and Test

* Jenkins Pipeline Execution:
* Clone Repository: Jenkins clones the repository from GitLab.
* Get Build Time: Jenkins retrieves the current time to tag the Docker image.
* Docker Login: Jenkins logs in to Docker Hub using credentials stored in Jenkins.
* Build Docker Image: Jenkins builds the Docker image for the Flask application.
* Test Docker Image: Jenkins runs tests on the newly built Docker image.

### Update Helm Chart

* Update Helm Chart:
* Jenkins updates the Helm chart with the new Docker image version.
* Push Helm Chart: Jenkins builds and pushes the updated Helm chart to the Helm repository.

### Push Docker Image

* Push Docker Image: Jenkins pushes the Docker image to Docker Hub.

### Continuous Deployment (CD) with ArgoCD

### Monitoring and Syncing

* ArgoCD Monitors Repositories: ArgoCD continuously monitors the GitLab repository for changes to the Helm charts and configurations.
* Detect Changes: When a new Docker image or Helm chart version is pushed, ArgoCD detects the changes.

### Deployment

* Sync with Desired State: ArgoCD syncs the Kubernetes cluster with the desired state defined in the GitLab repository.
* Automated Deployment: ArgoCD deploys the updated Helm chart, which includes the new Docker image, to the Kubernetes cluster.


## Cluster Configuration

####	**Setting up Kubernetes Cluster**:
* Depending on your preference and environment, choose Google Kubernetes Engine (GKE), Minikube, Kind, Docker Desktop Kubernetes Engine, or use Terraform with Kubespray for deployment on bare metal or any cloud provider.

#### **Install ArgoCD**
* Install ArgoCD on your Kubernetes cluster. ArgoCD will serve as our GitOps continuous deployment tool, automating the deployment of Helm charts and Docker images based on changes to Git repositories.

#### **Configure ArgoCD**
* Setup connection to Git repositories using SSH key. Define repositories, Helm charts, and Docker images that ArgoCD will monitor and synchronize with the desired state.
* Install root application, that serves as the central control point for managing our infrastructure and applications deployed on Kubernetes.  
Its main role is to orchestrate the deployment of other applications defined in Git repositories, ensuring they are automatically deployed and synchronized to their desired state.

#### **Configure Jenkins**  
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

To access the **Grafana** dashboard, you can use port forwarding:

```
kubectl port-forward --namespace kube-prometheus-stack svc/kube-prometheus-stack-grafana 3000:80
```

* Get your Grafana password

```
kubectl get secret --namespace kube-prometheus-stack grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```
Login is ```admin```
Password is  ```prom-operator```

You can checkout already preinstalled dashboards for monitoring all of the cluster.


### Configure Jenkins Pipeline

Let's access Jenkins 

```
kubectl get secret --namespace jenkins jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode ; echo
kubectl port-forward svc/jenkins 8080:8080 -n jenkins
```

Login is ```admin```
Password is ```4B6LzzwQUBFrhBKIi0e6Tu```

* Create new user.
**Manage Jenkins > Users > Create User** 

* Logout from root user and access to created one.

<img src="images/change-account-jenkins.png" width="700">

Now we need to provide our **docker** and **gitlab** credentials

I'm using Username and Password option, but instead of password I'll provide **GitLab Access Token**.

**Add GitLab credentails**
```
Manage Jenkins > Credentials > (global) > Add Credentials
Scope - Global
Username - GitLab Username
Password - GitLab Access Token
ID - gitlab-cred
Description - GitLab Credentials
```

**Add Docker credentials**  
Here I will also use Dockerhub Access Token

```
Scope - Global
Username - Docker Username
Password - DockerHub Access Token
ID - docker
Description - Docker Credentials
```

**Let's create a pipeline that will build Docker Image and change Helm chart to New version**

```
Create a job > Pipeline 
Skip all options until the **Pipeline**

Pick `Pipeline script from SCM`
SCM > Git
Repository URL > GitLab Repository 
Credentials > gitlab-cred

Branch Specifier > */<branch> Provide path to Jenkinsfile
```
**And click _Save_**

<img src="images/add-pipeline-scm.png" width="1000">

**Now when you want to build new image and update it on the clutser you can simply run job**

You can check **Jenkinsfile** under the **Spoiler** 
<details>
<summary>Jenkinsfile</summary>

```yaml
pipeline {
    agent {
        kubernetes {
            label 'kuberagent'
            defaultContainer 'jnlp'
            yamlFile 'agent.yaml'
        }
    }
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = 'saddff/flask_app'
    }
    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }
        stage('Get Build Time') {
            steps {
                script {
                    env.DOCKER_TAG = sh(script: 'date +%Y%m%d%H%M%S', returnStdout: true).trim()
                }
            }
        }
        stage('Docker Login') {
            steps {
                container('dind') {
                    withCredentials([usernamePassword(credentialsId: 'docker', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin $DOCKER_REGISTRY'
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                container('dind') {
                    sh 'docker build -t $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG .'
                }
            }
        }
        stage('Test Docker Image') {
            steps {
                container('dind') {
                    script {
                        sh 'docker run -d --rm -p 5000:5000 --name test-container $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG python test_app.py'
                    }
                }
            }
        }
        stage('Update Helm Chart') {
            steps {
                container('dind') {
                    script {
                        withCredentials([usernamePassword(credentialsId: 'gitlab-cred', usernameVariable: 'GITLAB_USERNAME', passwordVariable: 'GITLAB_PASSWORD')]) {
                            sh 'git config --global --add safe.directory /home/jenkins/agent/workspace/docker-pipeline'
                            sh 'git config --global user.email "tsorefdaniel@gmail.com"'
                            sh 'git config --global user.name "Autobot jenkins"'
                            sh 'git checkout -b dev'
                            sh 'sed -i "s/version:.*/version: $DOCKER_TAG/" flask_app/Chart.yaml'
                            sh 'sed -i "s|image: docker.io/saddff/flask_app:.*|image: docker.io/saddff/flask_app:$DOCKER_TAG|g" flask_app/values.yaml'
                            sh 'git add flask_app/Chart.yaml flask_app/values.yaml'
                            sh 'git commit -m "Automatic version update to version $DOCKER_TAG"'
                            sh 'git push https://${GITLAB_USERNAME}:${GITLAB_PASSWORD}@gitlab.com/sela-tracks/1099/students/saddff2/final-project/application.git dev'
                        }
                    }
                }
            }
        }
        stage('Build and Push Helm Chart') {
            steps {
                container('dind') {
                    script {
                        withCredentials([usernamePassword(credentialsId: 'docker', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                            sh '''
                            echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin $DOCKER_REGISTRY
                            helm package flask_app
                            helm push flask_app-${DOCKER_TAG}.tgz oci://registry-1.docker.io/saddff/
                            '''
                        }
                    }
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                container('dind') {
                    sh 'docker push $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }
    }
}
``` 
</details>

Also you can check **Dockerfile**

<details>
<summary>Dockerfile</summary>

```Dockerfile
FROM python:3.11.9-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "main.py"]

EXPOSE 5000
```
</details>

## Conclusion

Deploying and managing a Kubernetes cluster with automated CI/CD pipelines ensures that your infrastructure remains up-to-date and resilient.  
By using ArgoCD for GitOps-based continuous deployment, Jenkins and GitLab CI for CI/CD pipelines, and Grafana + Prometheus for monitoring, we have established a robust and scalable setup.  
This allows for streamlined code integration, automated testing, and deployment processes, along with comprehensive monitoring to maintain the health and performance of your applications and infrastructure.

## Final Result

By following this guide, you have successfully deployed a Kubernetes cluster that automates the deployment of a Flask application connected to MongoDB.  
With ArgoCD, Jenkins, GitLab CI, Grafana, and Prometheus integrated, you have a comprehensive solution that ensures continuous integration, continuous deployment, and real-time monitoring of your infrastructure and applications.  
This setup enhances efficiency, reduces manual intervention, and provides visibility into your system’s performance and health.

## Additional Resources

* [Kubernetes Documentation](https://kubernetes.io/docs/home/)
* [ArgoCD Documentation](https://argo-cd.readthedocs.io/en/stable/)
* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Kubespray Documentation](https://kubespray.io/#/)

## Next Steps

### Ingress Configuration

Set up an Ingress controller (like NGINX or Traefik) to manage external access to your services. Create Ingress resources to route traffic based on hostnames and paths, and configure TLS/SSL for secure communication.

### Security and Scalability

Implement Role-Based Access Control (RBAC) and network policies to enhance security. Configure the Horizontal Pod Autoscaler (HPA) and Cluster Autoscaler to automatically scale your applications and cluster based on resource needs.

### Terraform and Kubespray 

Develop a Terraform script to automate provisioning of Kubernetes cluster and use Kubespray for cluster deployment. Integrate Terraform and Kubespray for consistent infrastructure management.


## Thank You
Thank you for following along with this guide! I hope this has been helpful for your Kubernetes cluster deployment and management.  
