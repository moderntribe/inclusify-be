# Description

# Poject
https://console.cloud.google.com/functions/details/europe-west1/function-1?authuser=1&hl=es&project=degenderify&supportedpurview=project

# Production
https://europe-west1-degenderify.cloudfunctions.net/degenderify

## Deploy
```bash
git push --all google
```

# Development
- http://localhost:8080/?text=he%20was%20a%20great%20man
- http://localhost:8080/?text=he%20was%20a%20great%20man&pron=yay

```sh
functions-framework --target=degenderify_request
```