export SERVICE_NAME=dhohir

kubectl apply -n isolate-jupyter -f deployment.yaml
kubectl apply -n isolate-jupyter -f service.yaml

kubectl logs -l app=isolate-jupyter-dhohir -n isolate-jupyter | grep "token=" | awk -F"=" '{print $NF}' | tail -n 1
bash: $(kubectl logs -l app=isolate-jupyter-dhohir -n isolate-jupyter 2>&1 | grep "token=" | awk -F"=" '{print $NF}' | tail -n 1)
kubectl get svc isolate-jupyter-dhohir-service -n isolate-jupyter -o=jsonpath='{.spec.ports[0].nodePort}'
