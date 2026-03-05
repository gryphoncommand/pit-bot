#!/bin/bash

docker run -it --rm \
  -p 8000:8000 \
  -e "OPENAI_BASE_URL=http://host.docker.internal:1234/v1" \
  pit-bot:local
