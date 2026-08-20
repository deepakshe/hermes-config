#!/bin/bash
echo "Syncing local config with repository..."
git pull origin main
cp config.yaml ~/AppData/Local/hermes/config.yaml
