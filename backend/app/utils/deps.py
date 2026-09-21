from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CarePartner
from app.utils.security import decode_token

bearer_scheme = HTTPBearer()


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> CarePartner:
    payload = decode_token(creds.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid ya expire ho gaya",
        )

    user = db.query(CarePartner).filter(
        CarePartner.id == int(payload["sub"])
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User nahi mila")

    return user