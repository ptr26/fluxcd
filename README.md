minikube delete --all
minikube start -p fluxcd --kubernetes-version=latest
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

flux bootstrap github \
  --owner=ptr26 \
  --repository=fluxcd \
  --branch=main \
  --path=repositories/infra/clusters/my-cluster \
  --personal \
  --private=true
