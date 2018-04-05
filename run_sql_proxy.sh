#!/bin/sh

BASE=${HOME}/students
PROJ=csufchatbot
GCLOUD_PROJ=sample-project-196107
GCLOUD_REGION=us-east1
SECRET=secret_gcloud.json
#SECRET=sample-project-168fde2d1d92.json

cloud_sql_proxy -dir=/tmp -instances=${GCLOUD_PROJ}:${GCLOUD_REGION}:${PROJ} -credential_file=${SECRET}

