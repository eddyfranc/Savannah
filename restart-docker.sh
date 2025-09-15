#!/bin/bash

echo "🔴 Stopping Docker Desktop..."
taskkill //IM "Docker Desktop.exe" //F >/dev/null 2>&1

echo "🟢 Starting Docker Desktop..."
"/c/Program Files/Docker/Docker/Docker Desktop.exe" &

echo "⏳ Waiting for Docker to start..."
sleep 20  # wait 20s, adjust if your PC is slower

# check if Docker is ready
until docker info >/dev/null 2>&1; do
  echo "⚙️  Still waiting for Docker engine..."
  sleep 5
done

echo "✅ Docker is running!"
