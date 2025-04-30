from datetime import datetime, timedelta, timezone
from firebase_admin import firestore

db = firestore.client()

def set_premium(user_id: str, days: int = 30):
    """Otorga estado premium por X días."""
    premium_until = datetime.now(timezone.utc) + timedelta(days=days)
    premium_iso = premium_until.isoformat().replace("+00:00", "Z")

    db.collection("users").document(str(user_id)).set({
        "premium_until": premium_iso
    }, merge=True)

def is_premium(user_id: str) -> bool:
    """Verifica si un usuario es premium actualmente."""
    doc = db.collection("users").document(str(user_id)).get()
    if not doc.exists:
        return False

    data = doc.to_dict()
    premium_until = data.get("premium_until")
    if not premium_until:
        return False

    try:
        expiry = datetime.fromisoformat(premium_until.replace("Z", "+00:00"))
    except ValueError:
        return False

    return datetime.now(timezone.utc) < expiry

def get_premium_expiry(user_id: str) -> str:
    """Devuelve la fecha de expiración del premium (o None)."""
    doc = db.collection("users").document(str(user_id)).get()
    if not doc.exists:
        return None

    data = doc.to_dict()
    return data.get("premium_until")
