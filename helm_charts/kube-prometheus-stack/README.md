helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update

helm pull prometheus-community/kube-prometheus-stack

kubectl edit daemonset kube-prometheus-stack-prometheus-node-exporter -n kube-prometheus-stack

DELETE THIS 
# ... other container fields ...
volumeMounts:
- name: proc
  mountPath: /host/proc
  readOnly: true
- name: sys
  mountPath: /host/sys
  readOnly: true
# REMOVE THIS:
#- name: root
#  mountPath: /host/root
#  readOnly: true 
# ... other container fields ...
