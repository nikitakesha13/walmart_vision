Linux 

1. Install nvidia drivers on the computer
Check installation by running "nvidia-smi"
If drivers are not found, then search "additional drivers" and select the best nvidia driver
Or use commands "sudo ubuntu-drivers devices" and install recommended driver by running "sudo ubuntu-drivers install nvidia-driver-<recommended>"
2. Install docker engine 
3. Install nvidia docker 
4. Follow steps found here. 
5. Pull the docker image by running "sudo docker pull ..."
6. Enable clients to connect from any host by running "xhost +"
7. Run the docker image



