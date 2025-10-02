# Salt Lab
This repo is a small part of a larger GitOps workflow to manage Arista EOS configurations via Github. It contains the Salt master configuration for my private GNS3 lab. When changes are merged to this repo, a webhook is triggered toward an instance of Jenkins which is hosted in AWS. This triggers Jenkins to pull the files from this repo and deploy them to the Salt master, which is also hosted in AWS.

A number of Arista vEOS devices have been configured in a data center topology within GNS3. The topology is pictured below. The configurations found in /pillar are for Arista vEOS devices within this lab. A Salt minion extension has been installed and outbound connectivity from the lab to the internet has been configured. Therefore the Arista vEOS switches in this lab are able to be managed by the Salt master in AWS.

<img width="2172" height="975" alt="image" src="https://github.com/user-attachments/assets/8f368d37-0376-4510-9455-96ca6f0c7558" />


The network uses VXLAN, EVPN, and MLAG like many modern data centers.
