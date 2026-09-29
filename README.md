# Devkit CLI

Same engine for the CLI, HTTP API, and GitHub Action.

```
src/backend   engine + FastAPI   :8050
src/frontend  report UI          :3050
```

```bash
cd ~/devkit-cli/src/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.cli scan ../..
uvicorn app.main:app --reload --port 8050
```
