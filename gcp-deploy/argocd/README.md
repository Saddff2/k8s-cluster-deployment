kubectl create namespace argocd

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl port-forward svc/argocd-server 9101:80 -n argocd

**Getting password**
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode ; echo

add ssh key in argocd gui settings (you can do it also in CLI)


CREATE PV FOR FLASK-APP/MONGO-DB

gcp-deploy % gcloud compute disks create mongo-disk --size=10GB --zone=me-central1-a