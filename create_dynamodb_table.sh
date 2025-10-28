#!/usr/bin/env bash
set -e
TABLE_NAME=HotelRooms
aws dynamodb create-table --cli-input-json file://dynamodb/schema.json || true
echo "Sleeping to allow table creation..."
sleep 5
echo "Populating sample data (batch-write)"
aws dynamodb batch-write-item --request-items file://dynamodb/sample_data_batch_write.json
echo "Done."
