# Cluster Creation and Application Deployment with KIND
This README details the steps for recreating a KIND cluster specifically tailored for deploying the FastAPI application with custom port mappings.

## Prerequisites
* Docker and KIND installed on the VM.
* Kubernetes CLI (kubectl) installed and configured.
* Docker image of the FastAPI application ready to be deployed.
## Steps to Recreate the KIND Cluster
#### Delete Existing KIND Cluster
To ensure a clean setup, remove any existing clusters:
   ```
    kind delete cluster --name url-shortener
   ```
#### Create New KIND Cluster
Before initiating the cluster setup, it's important to tailor your kind-config.yaml file to match the specific networking requirements of your services. This includes defining the ports that need to be exposed:
* NodePort: Typically used for direct node access, e.g., 30080.
* Ingress: For HTTP and HTTPS traffic, ensure ports 80 and 443 are available.
* Load Balancing: Specify additional ports as required by your load balancer or other services.

Create a new cluster using a custom configuration to tailor the networking and resource allocations:
   ```
    kind create cluster --config kind-config.yaml --name url-shortener
   ```

#### Verify Cluster Creation
Check the details of the newly created cluster to ensure it's set up correctly:
   ```
    kubectl cluster-info --context kind-url-shortener
   ```

## Redeploy the Application
#### Load Docker Image into KIND
Import your Docker image into the KIND cluster:
   ```
    kind load docker-image url-shortener:latest --name url-shortener
   ```
#### Apply Kubernetes Manifests
Deploy your application using Kubernetes manifests. This can be done globally or by specifying individual files:
   ```
    cd k8s/base/
    # kubectl apply -f . (avoid to not deploy ingress also)
    # or
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
   ```
## Check NodePort Service
#### Verify the Service
Ensure that the Kubernetes service is running and correctly configured:
   ```
    kubectl get svc url-shortener
   ```
Look for the output to confirm the NodePort is exposed as expected (e.g., 80:30080/TCP).

*********

## Connecting Using NodePort and Port Forwarding
These methods allow external access to your FastAPI application running within the KIND cluster. Here’s how to set up and use both NodePort and Port Forwarding.

### NodePort Connection
NodePort exposes your service on each Node’s IP at a static port. The allocation of this port can be specified in the service definition.

##### External Access Configuration
To access your application externally from the host machine, modify the kind-config.yaml to include necessary port mappings under the appropriate nodes.
Example Configuration
   ```
    kind: Cluster
    apiVersion: kind.x-k8s.io/v1alpha4
    nodes:
    - role: control-plane
      extraPortMappings:
      - containerPort: 30080
        hostPort: 30080
        protocol: TCP
   ```
##### Service Configuration
Here’s how to set up a service of type NodePort:
   ```
    service:
      spec:
        type: NodePort
        ports:
        - port: 80
          targetPort: 80
          nodePort: 30080
   ```
#### Rapply Kubernetes Manifests
   ```
    cd k8s/base/
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
   ```
##### Check Pod Status
   ```
    kubectl get pods
   ```
* Ensure all pods are in Running status.
* Fix ImagePullBackOff Errors: Set imagePullPolicy: IfNotPresent to prevent Kubernetes from pulling the image from a registry if it exists locally.

##### Steps to Connect
Retrieve Node IP Addresses:
Use the following command to get the internal IP addresses of the nodes:
   ```
    kubectl get nodes -o wide
   ```
##### Access the Application Locally:
Use the internal IP with the node port to access the FastAPI application:
   ```
    curl http://<node-ip>:30080/docs (master or worker node)
    Example:
    curl http://172.18.0.3:30080/docs
   ```
##### Accessing from Host
Once the KIND cluster and NodePort are configured, you can access the FastAPI application via:
   ```
    http://<VM-ip>:<Node-Port>/docs
    Example:
    http://192.168.1.21:30080/docs
    or 
    http://url-shortener.local:30080/docs
   ```
### Port Forwarding
Port forwarding lets you redirect a network port from one address to another. This is useful for accessing services from your local machine.

##### Steps for Port Forwarding
Forward a Service:
To forward a service’s port to your local machine:
   ```
    kubectl port-forward svc/url-shortener 8080:80
   ```
Forward a Pod:
Alternatively, you can forward the port directly from a specific pod:
   ```
    kubectl port-forward url-shortener-9b99b4dc8-2pgws 8080:80
   ```
##### Access the Application Locally:
Once forwarding is set up, access the application using:
   ```
    curl localhost:8080/docs
   ```
Important Notes
The application Docker container should be configured to expose the appropriate port. In your FastAPI deployment, the Docker command might look like:
   ```
    CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
   ```
##### Accessing from Host
Once the KIND cluster and NodePort are configured, you can access the FastAPI application via:
   ```
    http://<VM-ip>:<Node-Port>/docs
    Example:
    http://192.168.1.21:30080/docs
        or 
    http://url-shortener.local:30080/docs
   ```
*********
## Connecting Using Ingress
Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster, offering fine-grained control over the traffic routing and external access. This section details configuring KIND to use NGINX as an Ingress controller and setting up the necessary resources.

##### Update KIND Configuration
First, modify the kind-config.yaml file to map the necessary ports for HTTP and HTTPS traffic:

   ```
    nodes:
      - role: control-plane
        extraPortMappings:
          - containerPort: 80
            hostPort: 80
            protocol: TCP
          - containerPort: 443
            hostPort: 443
            protocol: TCP
      - role: worker
  ```
##### Service Configuration
Here’s how to set up a service of type ClusterIP:
   ```
    service:
      spec:
        type: ClusterIP
        ports:
        - port: 80
          targetPort: 80
   ```
##### Install NGINX Ingress Controller
Deploy the NGINX Ingress Controller to manage ingress resources within your cluster:
   ```
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
   ```
#### Rapply Kubernetes Manifests
   ```
    cd k8s/base/
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    kubectl apply -f ingress.yaml
   ```
Monitor the Ingress Controller Deployment
Monitor the deployment process to ensure all components are up and running:
   ```
    kubectl get pods -n ingress-nginx --watch
   ```
##### Label the Nodes
Apply necessary labels to your nodes to designate them for ingress traffic handling:
   ```
    kubectl label node url-shortener-control-plane ingress-ready=true kubernetes.io/os=linux
    kubectl label node url-shortener-worker ingress-ready=true kubernetes.io/os=linux
   ```
Verify Node Labels
Confirm that the nodes are correctly labeled:
   ```
    kubectl get nodes --show-labels
   ```
You should see ingress-ready=true and kubernetes.io/os=linux in the output.
##### Check Pod Status
   ```
    kubectl get pods
   ```
* Ensure all pods are in Running status.
* Fix ImagePullBackOff Errors: Set imagePullPolicy: IfNotPresent to prevent Kubernetes from pulling the image from a registry if it exists locally.
##### Check Ingress Controller Pods
Ensure the Ingress controller pods have transitioned from Pending to Running status:
   ```
    kubectl get pods -n ingress-nginx
   ```
##### Create an Ingress Resource
Deploy an Ingress resource to expose your FastAPI application:
   ```
    kubectl apply -f ingress.yaml
   ```
Verify Ingress Resource
Check the status of the Ingress resource to confirm it's been successfully created:
   ```
    kubectl get ing
   ```
Expected output might look like this:
   ```
NAME                    CLASS    HOSTS                 ADDRESS     PORTS   AGE
url-shortener-ingress   <none>   url-shortener.local   localhost   80      3m33s
   ```

##### Configure Hosts File for Local Access
To access your application through a friendly URL, add an entry in your host machine's /etc/hosts file:
   ```
    sudo vi /etc/hosts
    192.168.1.21    url-shortener.local
   ```

##### Access the Application Locally:
Once forwarding is set up, access the application using:
   ```
    curl localhost:80/docs
    or just: curl localhost/docs
   ```

##### Accessing from Host
Now, you can access the FastAPI application through your browser using a URL that resolves locally:
   ```
    http://url-shortener.local/docs
   ```

### Install a DNS Server

* Following these steps, your domain `url-shortener.local` will resolve to `192.168.1.21` on your local network.
* This allows you to simulate a more realistic production environment without modifying the `/etc/hosts` file on each machine.

##### BIND9 Installation
Execute the following commands to update your system and install BIND9 along with its utilities:

  ```
    sudo apt update && sudo apt upgrade -y
    sudo apt install bind9 bind9-utils bind9-doc dnsutils
  ```

##### Configuration of the DNS Zone
Edit the BIND9 local configuration file:
  ```
    sudo vi /etc/bind/named.conf.local
  ```
Add the following lines to define a new DNS zone for url-shortener.local:
  ```
    zone "url-shortener.local" {
        type master;
        file "/etc/bind/db.url-shortener.local";
    };
  ```

##### Creation of the DNS Zone File
Copy the default zone file to create a new one for url-shortener.local:

  ```
    sudo cp /etc/bind/db.local /etc/bind/db.url-shortener.local
  ```
Edit the new zone file:
  ```
    sudo nano /etc/bind/db.url-shortener.local
  ```
Modify the file to look like this, replacing IP_DU_CLUSTER with 192.168.1.21:
  ```
    ;
    ; BIND data file for local loopback interface
    ;
    $TTL    604800
    @       IN      SOA     url-shortener.local. root.url-shortener.local. (
                                  2024062901     ; Serial
                             604800         ; Refresh
                              86400         ; Retry
                            2419200         ; Expire
                             604800 )       ; Negative Cache TTL
    ;
    @       IN      NS      url-shortener.local.
    @       IN      A       192.168.1.21
  ```

##### Restart BIND9
After modifying the configuration files, restart BIND9 to apply the changes:

  ```
    sudo systemctl restart bind9
  ```

##### Test the Configuration
Use dig or nslookup to test the resolution of your domain:
  ```
    dig url-shortener.local @127.0.0.1
  ```

## Additional Information
Configuration File (kind-config.yaml): This file contains specifics about network configurations, storage volumes, and other essential parameters that tailor the KIND cluster for your application needs.
Kubernetes Manifests: These files (deployment.yaml, service.yaml, etc.) define how your application and its services are deployed and managed in Kubernetes.
