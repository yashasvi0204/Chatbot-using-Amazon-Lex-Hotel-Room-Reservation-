import boto3
import os
from decimal import Decimal

dynamo = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
TABLE_NAME = os.getenv('DYNAMODB_TABLE', 'HotelRooms')
table = dynamo.Table(TABLE_NAME)

def lambda_handler(event, context):
    # Lex V2 event shape uses sessionState; adapt as necessary
    try:
        slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})
        room_type = slots.get('RoomType', {}).get('value', {}).get('interpretedValue')
        nights = int(slots.get('Nights', {}).get('value', {}).get('interpretedValue', 1))
    except Exception as e:
        return build_response('Failed to parse request', fulfilled=False)

    # Lookup room availability
    resp = table.get_item(Key={'roomType': room_type})
    item = resp.get('Item')
    if item and int(item.get('available', 0)) > 0:
        # Decrement available count (simple reservation)
        try:
            table.update_item(
                Key={'roomType': room_type},
                UpdateExpression='SET available = available - :dec',
                ExpressionAttributeValues={':dec': Decimal(1)}
            )
        except Exception as e:
            # If update fails, return failure
            return build_response('Sorry, could not finalize booking.', fulfilled=False)

        return build_response(f'Room booked for {nights} night(s) in {room_type} room. Thank you!', fulfilled=True)
    else:
        return build_response('Sorry, no rooms available for that type.', fulfilled=False)

def build_response(message, fulfilled=True):
    state = 'Fulfilled' if fulfilled else 'Failed'
    return {
        'sessionState': {
            'dialogAction': {'type': 'Close'},
            'intent': {'name': 'BookRoom', 'state': state}
        },
        'messages': [{
            'contentType': 'PlainText',
            'content': message
        }]
    }

# Local test harness
if __name__ == '__main__':
    evt = {
        'sessionState': {
            'intent': {
                'slots': {
                    'RoomType': {'value': {'interpretedValue': 'Deluxe'}},
                    'Nights': {'value': {'interpretedValue': '2'}}
                }
            }
        }
    }
    print(lambda_handler(evt, None))
