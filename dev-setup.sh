set -e

echo "🧑‍🔧 Setting up pre-commit..."
pip3 install --upgrade pip
pip3 install pre-commit
pre-commit install -f
echo "✨ pre-commit is now configured!"

echo "🧑‍🔧 Building Docker images..."
#!/bin/bash -e
docker-compose build
echo "✨ 🐳 Docker images built!"

docker-compose run --rm frontend npm i
mkdir -p frontend/static/node_modules/.vite/deps
cp frontend/node_modules/parquet-wasm/esm/arrow2_bg.wasm frontend/static/node_modules/.vite/deps