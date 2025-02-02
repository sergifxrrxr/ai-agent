#!/bin/bash

ollama serve &

ollama create ai-travel-agent -f Modelfile

sleep 5

wait $!