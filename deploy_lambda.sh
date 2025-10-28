#!/usr/bin/env bash
set -e
# Edit these variables
FUNCTION_NAME=hotel-booking-handler
ROLE_ARN=arn:aws:iam::123456789012:role/lambda-exec-role
ZIP_FILE=deployment.zip

# Package
cd lambda
zip -r ../$ZIP_FILE .
cd ..

# Create or update function
if aws lambda get-function --function-name $FUNCTION_NAME > /dev/null 2>&1; then
  aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://$ZIP_FILE
else
  aws lambda create-function --function-name $FUNCTION_NAME --runtime python3.9 --role $ROLE_ARN --handler booking_handler.lambda_handler --zip-file fileb://$ZIP_FILE
fi

echo "Deployed lambda $FUNCTION_NAME"
