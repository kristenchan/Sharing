library(AzureRMR)
library(AzureContainers)

#------------------------------
# create resource group
#------------------------------
#deployresgrp <- AzureRMR::get_azure_login('AAAAAAAAAAAAAAAAAAAAAAAAAAAA')$
#  get_subscription("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")$
#  create_resource_group("gcaadeploy", location="westus2")

gcaagrp <- get_azure_login('AAAAAAAAAAAAAAAAAAAAAAAAAAAA')$
  get_subscription("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")$
  get_resource_group("gcaadeploy")

# create container registry
deployreg_svc = deployresgrp$create_acr("deployregtest")
gcaa_svc = gcaagrp$create_acr("gcaaregistry")


# build image 'gcaa_plumber'
setwd('/Users/sun/Desktop/gcaa_plumber')
call_docker("build -t gcaa_plumber .")

# upload the image to Azure
gcaareg <- gcaa_svc$get_docker_registry(as_admin=TRUE)
gcaareg$push("gcaa_plumber")

# Azure Container Instances
gcaaaci <- gcaagrp$create_aci("gcaaaci",
                              image="gcaaregistry.azurecr.io/gcaa_plumber",
                              registry_creds=gcaareg,
                              cores=2, memory=8,
                              ports=aci_ports(8000))

#Check API
response <- httr::POST("http://gcaaaci.westus2.azurecontainer.io:8000/result",
                       body=list(taxno='68387705'), encode="json")
httr::content(response, simplifyVector=TRUE)


