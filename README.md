minikube delete --all
minikube start -p fluxcd --kubernetes-version=latest
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

flux bootstrap github \
  --owner=ptr26 \
  --repository=fluxcd \
  --branch=main \
  --path=repositories/infra/clusters/my-cluster \
  --personal \
  --private=true \
  --token-auth

kubectl -n default apply -f repositories/infra/apps/example-app/git.yaml
kubectl -n default apply -f repositories/infra/apps/example-app/kustomization.yaml

flux create secret git podinfo-auth \
    --url=ssh://git@github.com:ptr26/fluxcd \
    --private-key-file=./identity