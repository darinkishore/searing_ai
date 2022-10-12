deploy the application to the digitalocean apps platform.

it is deployed from the searing_ai `master` branch.
on deployment, the `npm run build` command is executed via github actions to build the frontend of the app.

## do specifics

the environment variables are set in the digitalocean dashboard.
the dockerfile is `dockerfile.web` and the docker-compose file is `deploy/app-spec.yml`. 

## github actions
tests aren't run yet. they should be. 

## local development
use the development branch for local development. the master branch is for deployment.

## deployment

the deployment is done via github actions. the `deploy` workflow is triggered on push to the master branch.