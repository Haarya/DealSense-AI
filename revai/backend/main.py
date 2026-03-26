from fastapi import FastAPI

app = FastAPI(title="RevAI API")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "revai"}