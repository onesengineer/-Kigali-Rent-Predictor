<<<<<<< HEAD
# Kigali Rent Predictor (Live + Mobile/IoT Ready)

### Overview
This app predicts Kigali rent using a trained sklearn model. It serves a self-hosted dashboard and JSON API endpoints.

## 🎯 Local run
1. `python -m pip install -r requirements.txt`
2. `python app.py`
3. Open `http://127.0.0.1:5000`

## 🐳 Docker run
1. `docker build -t kigali-rent .`
2. `docker run -p 5000:5000 kigali-rent`

## 🚀 Deploy on GitHub + Render (or other host)
1. Push to GitHub `git init`, `git add .`, `git commit -m "init"`, `git branch -M main`, `git remote add origin <URL>`, `git push -u origin main`
2. On Render: create new Web Service, connect repo, branch `main`, Docker, auto-deploy.
3. Use `https://<service>.onrender.com`.

## 🔐 Optional: GitHub Actions + Docker (CI)
Use this workflow in `.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.11
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Static check
        run: python -m py_compile app.py
      - name: Build Docker image
        run: docker build -t kigali-rent .

```

## 📦 API Endpoints (mobile/IoT)
- `POST /predict` with JSON:
  - `location`, `size_m2`, `year_built`, `num_rooms`, `near_main_road`, `water_available`, `electricity_available`
- `GET /history`
- `GET /statistics`

## 📱 Mobile client example (JavaScript)
```js
const resp = await fetch('https://<your-host>/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    location: 'Gisozi',
    size_m2: 120,
    year_built: 2015,
    num_rooms: 3,
    near_main_road: 1,
    water_available: 1,
    electricity_available: 1
  })
});
const result = await resp.json();
console.log(result);
```

## 🌐 IoT integration (Python)
```python
import requests

data = {
    'location': 'Gisozi',
    'size_m2': 100,
    'year_built': 2018,
    'num_rooms': 2,
    'near_main_road': 1,
    'water_available': 1,
    'electricity_available': 1
}

res = requests.post('https://<your-host>/predict', json=data)
print(res.json())
```

## 🧪 Standalone local HTML test page
1. Open `standalone.html` in browser (double-click).
2. Ensure backend is running: `python app.py`.
3. Fill form and click Predict.
4. Response appears in page output.

## 🔧 Notes
- Ensure `rent_model.pkl`, `scaler.pkl`, `columns.pkl` are present before startup.
- For real production, add HTTPS, request throttling, auth (API key/JWT) and model versioning.

## 🌍 Quick public testing with ngrok (mobile/IoT proof-of-concept)
1. Install ngrok: https://ngrok.com/download
2. Run your app locally: `python app.py` (or Docker)
3. In another terminal: `ngrok http 5000`
4. Use generated URL, e.g. `https://1234abcd.ngrok.io`

### Test from mobile/IoT
```bash
curl -X POST https://1234abcd.ngrok.io/predict \
  -H "Content-Type: application/json" \
  -d '{"location":"Gisozi","size_m2":120,"year_built":2015,"num_rooms":3,"near_main_road":1,"water_available":1,"electricity_available":1}'
```
- Replace with your ngrok URL and inspect response.
- Use same URL in React Native / Flutter `fetch` or ESP32 HTTP client.

=======
# Kigali Rent Predictor (Live + Mobile/IoT Ready)

### Overview
This app predicts Kigali rent using a trained sklearn model. It serves a self-hosted dashboard and JSON API endpoints.

## 🎯 Local run
1. `python -m pip install -r requirements.txt`
2. `python app.py`
3. Open `http://127.0.0.1:5000`

## 🐳 Docker run
1. `docker build -t kigali-rent .`
2. `docker run -p 5000:5000 kigali-rent`

## 🚀 Deploy on GitHub + Render (or other host)
1. Push to GitHub `git init`, `git add .`, `git commit -m "init"`, `git branch -M main`, `git remote add origin <URL>`, `git push -u origin main`
2. On Render: create new Web Service, connect repo, branch `main`, Docker, auto-deploy.
3. Use `https://<service>.onrender.com`.

## 🔐 Optional: GitHub Actions + Docker (CI)
Use this workflow in `.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.11
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Static check
        run: python -m py_compile app.py
      - name: Build Docker image
        run: docker build -t kigali-rent .

```

## 📦 API Endpoints (mobile/IoT)
- `POST /predict` with JSON:
  - `location`, `size_m2`, `year_built`, `num_rooms`, `near_main_road`, `water_available`, `electricity_available`
- `GET /history`
- `GET /statistics`

## 📱 Mobile client example (JavaScript)
```js
const resp = await fetch('https://<your-host>/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    location: 'Gisozi',
    size_m2: 120,
    year_built: 2015,
    num_rooms: 3,
    near_main_road: 1,
    water_available: 1,
    electricity_available: 1
  })
});
const result = await resp.json();
console.log(result);
```

## 🌐 IoT integration (Python)
```python
import requests

data = {
    'location': 'Gisozi',
    'size_m2': 100,
    'year_built': 2018,
    'num_rooms': 2,
    'near_main_road': 1,
    'water_available': 1,
    'electricity_available': 1
}

res = requests.post('https://<your-host>/predict', json=data)
print(res.json())
```

## 🧪 Standalone local HTML test page
1. Open `standalone.html` in browser (double-click).
2. Ensure backend is running: `python app.py`.
3. Fill form and click Predict.
4. Response appears in page output.

## 🔧 Notes
- Ensure `rent_model.pkl`, `scaler.pkl`, `columns.pkl` are present before startup.
- For real production, add HTTPS, request throttling, auth (API key/JWT) and model versioning.

## 🌍 Quick public testing with ngrok (mobile/IoT proof-of-concept)
1. Install ngrok: https://ngrok.com/download
2. Run your app locally: `python app.py` (or Docker)
3. In another terminal: `ngrok http 5000`
4. Use generated URL, e.g. `https://1234abcd.ngrok.io`

### Test from mobile/IoT
```bash
curl -X POST https://1234abcd.ngrok.io/predict \
  -H "Content-Type: application/json" \
  -d '{"location":"Gisozi","size_m2":120,"year_built":2015,"num_rooms":3,"near_main_road":1,"water_available":1,"electricity_available":1}'
```
- Replace with your ngrok URL and inspect response.
- Use same URL in React Native / Flutter `fetch` or ESP32 HTTP client.

>>>>>>> 64d109b (fix port issue and add /test endpoint)
