import random
import string
from .models import SessionMember


def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def add_user_to_session(session, user, role="PLAYER"):
    return SessionMember.objects.get_or_create(
        session=session,
        user=user,
        defaults={"role": role}
    )