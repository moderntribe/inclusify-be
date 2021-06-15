# Inclusify Backend

Remove biases from your texts.

Build a more inclusive world, word by word.

![Inclusify Screenshot](https://user-images.githubusercontent.com/779993/122103587-b23ae400-ce0e-11eb-918f-7a2a81b541db.png)

> Prototype by Modern Tribe as part of our Day of Action 2021.

# Description

AI system capable to remove any personal data such as names, locations and gender.
It uses NLP pipelines to extract and replace that information.
Next developments will include remove images/faces from documents, etc.

# Production endpoint
https://europe-west1-degenderify.cloudfunctions.net/degenderify

## Deploy
```bash
git push --all google
```
# Development
- http://localhost:8080/?text=he%20was%20a%20great%20man
- http://localhost:8080/?text=he%20was%20a%20great%20man&pron=yay
## Run locally
```sh
functions-framework --target=degenderify_request
```