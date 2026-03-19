Write-Host "Starting Bhoomi Drishti Backend..."
Start-Process powershell -ArgumentList "-NoExit","-Command","cd backend; if (-not (Test-Path .env)) { Copy-Item .env.example .env }; python -m venv venv; .\venv\Scripts\python -m pip install -r requirements.txt; .\venv\Scripts\uvicorn app.main:app --reload"

Write-Host "Starting Bhoomi Drishti Frontend..."
Start-Process powershell -ArgumentList "-NoExit","-Command","cd frontend; npm install; npm run dev"

Write-Host "Started frontend and backend in new windows. You can access the app at http://localhost:3000"
