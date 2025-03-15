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

kubectl -n guest-book apply -f repositories/infra/apps/guest-book/git.yaml
kubectl -n guest-book apply -f repositories/infra/apps/guest-book/kustomization.yaml

minikube service example-app --url -n example-app --profile fluxcd
minikube service nginx-guestbook-service --url -n guest-book --profile fluxcd


minikube addons enable ingress -p fluxcd
minikube tunnel -p fluxcd