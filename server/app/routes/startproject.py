from fastapi import APIRouter, status, HTTPException, BackgroundTasks,Request
from app.models.start_project import StartProject
from app.db import table
from datetime import datetime
from app.emailserve.email_service import send_email
import uuid
from botocore.exceptions import ClientError
from app.limiter.rate_limter import rate_limit

router = APIRouter(prefix="/start-project", tags=["Start Project"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_project(
    data: StartProject,
    request: Request,
    background_tasks: BackgroundTasks
):
    client_ip = request.client.host

    created_at = datetime.utcnow().isoformat()
    allowed, message = rate_limit(f"startproject:{client_ip}")

    if not allowed:
        return {
            
            "detail": message
        }
    

    item = {
        "pk": "SUBMISSION#PROJECT",
        "sk": f"{created_at}#{uuid.uuid4()}",
        "entity": "PROJECT",
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

        #
        background_tasks.add_task(
            send_email,
            data.email,
            "We received your project request 🚀",
            (
                f"Hi {data.fullname},\n\n"
                "Thanks for sharing your project details with us. "
                "Our team is reviewing your requirements and will get back to you soon.\n\n"
                "Best regards,\nTeam \nTeclury"
            )
        )

 
        background_tasks.add_task(
            send_email,
            "manushn001@gmail.com",
            "New Project Request",
            (
                f"New project submission\n\n"
                f"Name: {data.fullname}\n"
                f"Company: {data.company}\n"
                f"Email: {data.email}\n"
                f"Phone: {data.phone}\n\n"
                f"Project Type: {data.type}\n"
                f"Budget: {data.budget}\n\n"
                f"Details:\n{data.projectdetails}"
            )
        )

        background_tasks.add_task(
            send_email,
            "bharathrajibs@gmail.com",
            "New Project Request",
            (
                f"New project submission\n\n"
                f"Name: {data.fullname}\n"
                f"Company: {data.company}\n"
                f"Email: {data.email}\n"
                f"Phone: {data.phone}\n\n"
                f"Project Type: {data.type}\n"
                f"Budget: {data.budget}\n\n"
                f"Details:\n{data.projectdetails}"
            )
        )

        return {
            "message": "Project details saved successfully"
        }

    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"DynamoDB error: {e.response['Error']['Message']}"
        )
