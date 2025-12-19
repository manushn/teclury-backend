from fastapi import APIRouter, status, HTTPException, Query, Header, Request
from typing import Optional
from jose import jwt, JWTError, ExpiredSignatureError
import base64, json, os
from app.db import table

router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")



def encode_cursor(key: dict) -> str:
    return base64.b64encode(json.dumps(key).encode()).decode()

def decode_cursor(cursor: str) -> dict:
    return json.loads(base64.b64decode(cursor.encode()).decode())



def verify_admin_token(authorization: str | None):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization format"
        )

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return payload



@router.get("/admin/submissions", status_code=status.HTTP_200_OK)
async def get_submissions(
    request: Request,  
    submission_type: str = Query(..., description="CONTACT | PROJECT | EARLY_ACCESS"),
    limit: int = Query(10, le=50),
    cursor: Optional[str] = None,
    authorization: Optional[str] = Header(None, alias="Authorization")
):
    
    verify_admin_token(authorization)

    pk_map = {
        "CONTACT": "SUBMISSION#CONTACT",
        "PROJECT": "SUBMISSION#PROJECT",
        "EARLY_ACCESS": "SUBMISSION#EARLY_ACCESS"
    }

    if submission_type not in pk_map:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid submission_type"
        )

    query_params = {
        "KeyConditionExpression": "pk = :pk",
        "ExpressionAttributeValues": {
            ":pk": pk_map[submission_type]
        },
        "Limit": limit,
        "ScanIndexForward": False
    }

    if cursor:
        query_params["ExclusiveStartKey"] = decode_cursor(cursor)

    response = table.query(**query_params)

    return {
        "items": response.get("Items", []),
        "next_cursor": encode_cursor(response["LastEvaluatedKey"])
        if "LastEvaluatedKey" in response else None
    }
