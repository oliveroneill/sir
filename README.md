# Sir - Serverless Invitation Response
A set of AWS Lambda handlers for allowing invitees to RSVP online.

## Deployment
You can use [pal](https://github.com/oliveroneill/pal) to package up the
modules with its dependencies. This will package up what's needed into
`package.zip`:
```bash
pal --dockerizePip --usePipenv -z
```
You can then use these commands to launch the AWS Lambdas:
```bash
aws lambda create-function --function-name enter_invite --zip-file fileb://package.zip --role arn:aws:iam::ACCOUNT_ID:role/lambda_dynamodb  --handler enter_invite.invite_form --runtime python3.6 --timeout 15 --memory-size 128
aws lambda create-function --function-name rsvp_details --zip-file fileb://package.zip --role arn:aws:iam::ACCOUNT_ID:role/lambda_basic_execution  --handler check_invitation_code.check_invitation_code --runtime python3.6 --timeout 15 --memory-size 128
aws lambda create-function --function-name respond --zip-file fileb://package.zip --role arn:aws:iam::ACCOUNT_ID:role/lambda_dynamodb  --handler rsvp.rsvp --runtime python3.6 --timeout 15 --memory-size 128
```

You can then direct users to the `enter_invite` Lambda to enter their invite code.

## Slack Logging
You can get updates when users RSVP via Slack. To do this, set environment
variables `SLACK_API_TOKEN` and `SLACK_CHANNEL_NAME`. Leaving these blank
will disable logging.

## Spotify Autocomplete
The UI has the option of autocompleting song searches. To use this set
the environment variable `SPOTIFY_CLIENT_SECRET`. This should be set to
a base64 encoding of `client_id:client_secret`. See the [Spotify docs](https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow) for more info.

## TODO
- Automatic deployment
