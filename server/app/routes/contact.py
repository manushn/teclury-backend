from fastapi import APIRouter, status, HTTPException, BackgroundTasks
from app.models.contact import contactModel as Contact
from app.db import table
from datetime import datetime
from app.emailserve.email_service import send_email
import uuid
from botocore.exceptions import ClientError

router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_contact(
    data: Contact,
    background_tasks: BackgroundTasks
):
    created_at = datetime.utcnow().isoformat()

    item = {
        "pk": "SUBMISSION#CONTACT",
        "sk": f"{created_at}#{uuid.uuid4()}",
        "entity": "CONTACT",
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
            "Thank you for contacting us",
            (
                f"Dear {data.name},\n\n"
                "Thank you for reaching out to us. "
                "We have received your message and will get back to you shortly.\n\n"
                "Best regards,\nTeam \nTeclury"
            )
        )

       
        background_tasks.add_task(
            send_email,
            "manushn001@gmail.com",
            "New Contact Submission",
            (
                f"New message from {data.name}\n\n"
                f"{data.message}\n\n"
                f"Email: {data.email}\n"
                f"Phone: {data.phone}"
            )
        )

        background_tasks.add_task(
            send_email,
            "bharathrajibs@gmail.com",
            "New Contact Submission",
            (
                f"New message from {data.name}\n\n"
                f"{data.message}\n\n"
                f"Email: {data.email}\n"
                f"Phone: {data.phone}"
            )
        )

        return {
            "message": "Contact saved successfully"
        }

    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"DynamoDB error: {e.response['Error']['Message']}"
        )
