import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from pydantic import BaseModel

# Initialize Firebase Admin SDK
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")
if not os.path.exists(cred_path):
    raise FileNotFoundError(f"Firebase credentials file not found at: {cred_path}")

cred = credentials.Certificate(cred_path)
firebase_app = firebase_admin.initialize_app(cred)

app = FastAPI()
bearer_scheme = HTTPBearer()


class ChatRequest(BaseModel):
    session_id: str
    message: str


# Create a dependency that verifies the Firebase token
def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        # The token is sent from the frontend in the Authorization header
        id_token = creds.credentials
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# --- Example of a Protected Endpoint ---
@app.post("/sell/conversation")
async def handle_selling_chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),  # This protects the endpoint!
):
    """
    Handles the multi-turn conversation for creating a new listing.
    Only authenticated users can access this.
    """
    user_uid = current_user["uid"]
    user_email = current_user["email"]

    # Now you can use the user's UID and email in your agent logic
    # For example, to save the listing under their ID.

    # response = listing_coordinator_agent.send(...)
    return {"reply": f"Authenticated as {user_email}", "session_id": request.session_id}
