from fastapi import APIRouter, status, HTTPException, BackgroundTasks
from app.models.early_access import EarlyAccess
from app.db import table
from datetime import datetime
from app.emailserve.email_service import send_email
import uuid
from botocore.exceptions import ClientError

router = APIRouter(prefix="/early-access", tags=["Early Access"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_early_access(
    data: EarlyAccess,
    background_tasks: BackgroundTasks
):
    created_at = datetime.utcnow().isoformat()

    item = {
        "pk": "SUBMISSION#EARLY_ACCESS",
        "sk": f"{created_at}#{uuid.uuid4()}",
        "entity": "EARLY_ACCESS",
        "created_at": created_at,
        **data.dict()
    }

    try:
        response = table.put_item(Item=item)

        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="DynamoDB write failed"
            )

        
        background_tasks.add_task(
            send_email,
            data.email,
            "You're on the Early Access list 🎉",
            f"Hi {data.name},\n\n"
            "Thanks for signing up for early access. "
            "We’ll notify you as soon as we launch.\n\n"
            "Best regards,\nTeam\nTeclury"
        )

       
        background_tasks.add_task(
            send_email,
            "manushn001@gmail.com",
            "New Early Access Signup",
            f"New early access request\n\n"
            f"Name: {data.name}\n"
            f"Email: {data.email}"
        )
        background_tasks.add_task(
            send_email,
            "bharathrajibs@gmail.com",
            "New Early Access Signup",
            f"New early access request\n\n"
            f"Name: {data.name}\n"
            f"Email: {data.email}"
        )

        return {
            "message": "Early access request saved successfully"
        }

    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"DynamoDB error: {e.response['Error']['Message']}"
        )
