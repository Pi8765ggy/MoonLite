python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cd frontend

npm install
npm run build

cd ..

mkdir moonlite/dist
cp -r frontend/dist/* moonlite/dist

flask --app moonlite init-db
