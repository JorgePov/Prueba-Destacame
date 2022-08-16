#!/bin/sh

echo "Run Frontend"

npm install --location=global esbuild 
npm --verbose install 
npm run dev