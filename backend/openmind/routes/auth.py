from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response

from pydantic import BaseModel

router = APIRouter()

# @router.post("/signin")
# async def signin(request: Request, response: Response, form_data: SignInForm):
#     return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)