# Architecture Overview

ASCII diagram (simple):

    +--------------+        +------------+        +------------+
    |  Client UI   | <----> | Amazon Lex | <----> | AWS Lambda |
    | (web/mobile) |        |  (Bot)     |        | (booking)  |
    +--------------+        +------------+        +------------+
                                        |
                                        v
                                   +-----------+
                                   | DynamoDB  |
                                   | (HotelRooms)|
                                   +-----------+

Components:
- Amazon Lex (V2) bot: handles NLU, slot-filling, and conversation state.
- AWS Lambda: business logic to check availability and make bookings in DynamoDB.
- DynamoDB: stores room types, prices, and availability.
- Optional: API Gateway / Cognito for authenticated Web UI integration.

Deployment notes:
- Use IAM roles with least privilege for Lambda and Lex.
- For web UI, use Cognito IdentityPool to provide temporary credentials to call Lex runtime.
- In production, add monitoring (CloudWatch), throttling, and transactional booking logic (e.g., conditional writes).
