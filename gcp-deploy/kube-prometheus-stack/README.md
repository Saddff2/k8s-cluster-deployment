helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update

helm pull prometheus-community/kube-prometheus-stack --untar

kubectl edit daemonset kube-prometheus-stack-prometheus-node-exporter -n kube-prometheus-stack

DELETE THIS IN charts/prometheus-node-exporter/templates/daemonset.yaml


{{- if .Values.hostRootFsMount.enabled }}
- name: root
  mountPath: /host/root
  {{- with .Values.hostRootFsMount.mountPropagation }}
  mountPropagation: {{ . }}
  {{- end }}
  readOnly: true
{{- end }}


{{- if .Values.hostRootFsMount.enabled }}
- name: root
  hostPath:
    path: /
{{- end }}




in argocd SERVER-SIDE APPLY FOR APPLICATION