provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
  }
}

resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  namespace  = kubernetes_namespace.argocd.metadata[0].name

  values = [
    <<EOF
    server:
      service:
        type: ClusterIP
    EOF
  ]
  set {
    name  = "server.ingress.enabled"
    value = "true"
  }

  set {
    name  = "server.service.type"
    value = "ClusterIP"
  }
}


