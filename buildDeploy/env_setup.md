STEP 0: login to docker repo
```
docker login -u raviupadhyaybkn
dckr_pat_qmwXgj2c4yj-2TomOexJUbffI7w
```

STEP 1: Pre-requisite [Docker] installed on macbook
STEP 2: Install minikube 
```
brew install minikube helm
minikube status
minikube start
```
Check zookeeper and kafka running using below command:
```
kubectl get pod -A 
NAMESPACE                       NAME                                          READY   STATUS    RESTARTS       AGE
kube-system                     coredns-787d4945fb-w6sr5                      1/1     Running   1 (110s ago)   3h8m
kube-system                     etcd-minikube                                 1/1     Running   1 (114s ago)   3h9m
kube-system                     kube-apiserver-minikube                       1/1     Running   1 (113s ago)   3h9m
kube-system                     kube-controller-manager-minikube              1/1     Running   1 (114s ago)   3h9m
kube-system                     kube-proxy-hcpft                              1/1     Running   1 (114s ago)   3h8m
kube-system                     kube-scheduler-minikube                       1/1     Running   1 (114s ago)   3h9m
kube-system                     storage-provisioner                           1/1     Running   1 (114s ago)   3h9m
my-cluster-operator-namespace   my-cluster-entity-operator-77555f78d6-2qkzr   1/3     Running   4 (21s ago)    128m
my-cluster-operator-namespace   my-cluster-kafka-0                            1/1     Running   2 (14s ago)    129m
my-cluster-operator-namespace   my-cluster-kafka-1                            1/1     Running   2 (16s ago)    129m
my-cluster-operator-namespace   my-cluster-kafka-2                            1/1     Running   2 (15s ago)    129m
my-cluster-operator-namespace   my-cluster-zookeeper-0                        1/1     Running   2 (15s ago)    129m
my-cluster-operator-namespace   my-cluster-zookeeper-1                        1/1     Running   2 (17s ago)    129m
my-cluster-operator-namespace   my-cluster-zookeeper-2                        1/1     Running   2 (14s ago)    129m
my-cluster-operator-namespace   strimzi-cluster-operator-ffdc9b669-dxv4g      1/1     Running   1 (113s ago)   133m

```

STEP 2: to deploy zookeeper and kafka

https://strimzi.io/docs/operators/latest/deploying.html#deploying-cluster-operator-str

FOLLOW:
=> 5.2.4. Deploying the Cluster Operator to watch all namespaces





IMAGE BUILD:
```
FROM python:latest
RUN apt-get update; apt-get install vim tmux -y
RUN pip3 install kafka-python flask-expects-json Flask[async] flask_socketio gunicorn  eventlet
ADD backendService /backendService
CMD ["/bin/sleep","1000000"]
ENTRYPOINT ["/usr/local/bin/python3","/backendService/flaskr/app.py"]
```