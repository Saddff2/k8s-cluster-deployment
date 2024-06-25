helm repo add jenkins https://charts.jenkins.io
helm repo update

helm pull jenkins/jenkins --untar install 

kubectl port-forward svc/jenkins 8080:8080 -n jenkins

kubectl get secret --namespace jenkins jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode