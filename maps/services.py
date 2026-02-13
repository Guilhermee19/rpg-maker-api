from sessions.models import SessionMember

def assert_member(session_id, user):
    return SessionMember.objects.filter(session_id=session_id, user=user).exists()

def assert_gm(session, user):
    return session.gm_id == user.id