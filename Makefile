build:
	docker build -t raviupadhyaybkn/meetuprsvp:v2 .
push:
	docker push raviupadhyaybkn/meetuprsvp:v2
remove:
	docker rmi raviupadhyaybkn/meetuprsvp:v2
rmdestroy:
	kubectl delete -f /Users/so43cs/Developer/PRO-Development/req-10053848/buildDeploy/3-k8sDeployment/pyhton_appDeployment.yaml 
deploy:
	kubectl apply -f /Users/so43cs/Developer/PRO-Development/req-10053848/buildDeploy/3-k8sDeployment/pyhton_appDeployment.yaml 
# all:
#     kubectl delete -f /Users/so43cs/Developer/PRO-Development/req-10053848/buildDeploy/3-k8sDeployment/pyhton_appDeployment.yaml .
# 	kubectl delete svc  my-app
# 	docker rmi raviupadhyaybkn/meetuprsvp:v2
# 	docker build -t raviupadhyaybkn/meetuprsvp:v2 .
# 	docker push raviupadhyaybkn/meetuprsvp:v2
# 	kubectl apply -f /Users/so43cs/Developer/PRO-Development/req-10053848/buildDeploy/3-k8sDeployment/pyhton_appDeployment.yaml 