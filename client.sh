#!/bin/bash

AUTH_TOKEN="<yourAuthToken>"

tipData=$(cardano-cli query tip --mainnet)
block=$(jq '.block' <<< "$tipData")

curl -s -X POST -H "Content-Type: application/json" -H "Auth: $AUTH_TOKEN" -d '{
  "id": '"$AUTH_TOKEN",
  "block": '"$block"'
}' http://localhost:5000/metrics
