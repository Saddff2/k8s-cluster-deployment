kubectl create namespace argocd


kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml


kubectl port-forward argocd-server 9101:443 -n argocd

**Getting password**
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode ; echo

argocd login localhost:9101 --username admin --password jfpNZz7EbpYrOT-C --insecure