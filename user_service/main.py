from fastapi import FastAPI


app = FastAPI(debug=True)


@app.get('/')
async def index() -> str:
    return f"User service! UPDATED"
