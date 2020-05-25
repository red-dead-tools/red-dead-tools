pushd gcloud-functions
gcloud functions deploy red_dead_tools --runtime python37 --trigger-http --allow-unauthenticated  --region europe-west2
popd
