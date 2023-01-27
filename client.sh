#!/bin/bash

AUTH_TOKEN="<yourAuthToken>"

tipData=$(cardano-cli query tip --mainnet 2> errors.txt)

if [ $? -ne 0 ]; then
   echo "$tipData is an invalid command."
else
   echo "$cmd_name is a valid command."
   block=$(jq '.block' <<< "$tipData")
   curl -s -X POST -H "Content-Type: application/json" -H "Auth: $AUTH_TOKEN" -d '{
  "id": '"$AUTH_TOKEN"',
  "block": '"$block"'
}' http://localhost:5000/metrics
fi


