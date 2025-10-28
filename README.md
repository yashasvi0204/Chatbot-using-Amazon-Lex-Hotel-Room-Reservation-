Deployment scripts notes:
- Edit `scripts/deploy_lambda.sh` to set ROLE_ARN and AWS account details.
- `create_dynamodb_table.sh` will create the table and bulk insert sample data.
- `deploy_lex.sh` is a placeholder because Lex deployments are often manual or require CloudFormation/SAM.
