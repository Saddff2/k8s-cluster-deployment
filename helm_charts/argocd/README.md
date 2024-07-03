terraform init

terraform apply

kubectl port-forward svc argocd-server 9101:80 -n argocd

**Getting password**
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode ; echo

add ssh key in argocd gui settings (you can do it also in CLI)