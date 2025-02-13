# AC295-practium1
## Introduction
In this practicum, we developed an art search engine that has 2 basic functionalities, ‘the simple query’ and ‘the similarity query’. We also implement 3 extra features. The first one is, rather than two frontends, we deploy everything with **one frontend**. The second one is that a **new metric** generated by an autoencoder is implemented to get similar images. The third one is that we can handle **additional queries** by having users inputting artist name and/or collection and/or genre.

## Video Link
https://drive.google.com/file/d/13YF0YeyHZzra38ht-s9cJEgAjwFrD1pr/view?ts=5f7bd6a9

## To run
0. Preparation    
\
Please have **google cloud platform command line, kubernetes, docker**, etc. ready on your machines.   

1. Setting up for google cloud platform    
\
`$export PROJECT_ID=example`  
Please substitute the `example` with specific GCP project ID.  
\
`$eval $(minikube -u minikube docker-env)`    
Set the docker daemon back to your machine.   
\
`$gcloud config list`  
Check google account    
\
`$gcloud auth configure-docker`    
Enable google container registry    

2. Building docker image  
\
`$docker build -t gcr.io/${PROJECT_ID}/webapp:db -f Docker_maindb .`  
`$docker build -t gcr.io/${PROJECT_ID}/task:frontend -f Docker_frontend .`  
Make sure to run these two lines in correct directory.      

3. Push docker image to registry  
\
`$docker push gcr.io/${PROJECT_ID}/webapp:db`      
`$docker push gcr.io/${PROJECT_ID}/task:frontend`      

4. Create cluster    
\
`$gcloud container clusters create cluster_name --num-nodes 2 --zone us-central1-a`    
The `cluster_name`, number of nodes, and zone are subject to changes.    

5. Deployment of kubernetes    
\
`$kubectl apply -f webapp_configmap.yaml`    
`$kubectl apply -f webapp_db_deployment_k8s.yaml`    
`$kubectl apply -f task_deployment_k8s.yaml`    
Make sure to run these lines in the correct directory.     
Also please change the project ID in `*_k8s.yaml` files.

6. Using the art search engine    
\
`$kubectl get all`    
Find the external IP from the output, for example `35.192.33.97`.   
To use "simple query", copy the URL `35.192.33.97:8081/GetImage` and paste in a web browser.  
To use "similarity query", copy the URL `35.192.33.97:8081/SimilarImage` and paste in a web browser.     

7. Don't forget to delete your GCP clusters.   
\
Either run `$gcloud container clusters delete cluster_name` or delete the cluster on GCP console.
    
# Good Luck!










