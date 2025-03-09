minikube start -p fluxcd --kubernetes-version=latest
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

flux bootstrap github \
  --owner=ptr26 \
  --repository=fluxcd \
  --branch=main \
  --path=clusters/my-cluster \
  --personal
