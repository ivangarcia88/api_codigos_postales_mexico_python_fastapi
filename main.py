import sys
import json
import uvicorn
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
if sys.version_info.minor < 10:
    import modauth39 as ma
else:
    import modauth as ma

tags_metadata = [
    {
        "name": "login",
        "description": "Login to use endpoint password/code, (user: juan, password:123)."
    },
    {
        "name": "code",
        "description": "Get information about a postal code (México), doesn't requiere authentication"
    },
    {
        "name": "code_password",
        "description": "Get information about a postal code (México), requieres authentication."
    }
]

with open("codigos_postales_reduced.json", encoding='utf-8') as f:
    data = f.read()
postal_code_database = json.loads(data)
app = FastAPI(openapi_tags=tags_metadata)

@app.post("/token", response_model=ma.Token, tags=["login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = ma.authenticate_user(ma.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ma.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = ma.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/code/{postal_code}", tags=["code"])
async def get_info(postal_code):
    global postal_code_database
    if postal_code in postal_code_database["codigos_postales"]:
        return postal_code_database["codigos_postales"][postal_code]
    else:
        return {"message:": f"El código postal {postal_code} no existe"}

@app.get("/password/code/{postal_code}", tags=["code_password"])
async def get_info(postal_code, current_user: ma.User = Depends(ma.get_current_active_user)):
    global postal_code_database
    if postal_code in postal_code_database["codigos_postales"]:
        return postal_code_database["codigos_postales"][postal_code]
    else:
        return {"message:": f"El código postal {postal_code} no existe"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)