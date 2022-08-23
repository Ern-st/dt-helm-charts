# helm-charts
This is our mono repository that contains all of our charts.

### Adding a Helm chart
If you would like to add a new service or Helm chart in general to this repository, please follow these steps carefully. 
1. Add a new folder to the charts/ directory named after your Helm chart. 
2. Inside this new folder, add a chart/ folder and put your Helm chart in there
3. Next to this new chart/ folder, add a README.md file and document the chart
4. It is important that you have a values.yaml file in the chart/ folder, even if it is empty, since the linter will otherwise fail
5. If you have any dependencies from a new helm repo that is not currently on the list in the follow files, you need to add it to the lists in the following files: 
   1. /.github/configs/ct-install.yaml under the "chart-repos" section
   2. /.github/configs/ct-lint.yaml under the "chart-repos" section
   3. /.github/workflows/publish.yaml under the step "Add dependency chart repos"

### Building docker images
To include a docker container and have it build and push to the local image registry on github, do the following: 
1. In the folder of your service, create a `container/` folder
2. Place your Dockerfile in the `container/` folder so it will be placed at `helm-charts/charts/<your-service>/container/Dockerfile`
3. Your docker image version will be the same version as your Helm chart, so remember to bump the Helm chart version when you want to update your Dockerfile

Note: Since development is dependent on this feature being implemented, in the first implementation, any push to main will trigger all Dockerfiles to be built. This will be changed in a later version so only the changed Dockerfiles are rebuilt. 
