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

## TODO
- Unit testing
- Automatic deployment
