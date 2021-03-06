from .models import (
    DBSession,
    Rower,
    )

def group_finder(username, request):
    try:
        rower = DBSession.query(Rower).filter_by(username=username).one()
        groups = ['group:members']
        if rower.admin:
            groups.append('group:admins')
        return groups
    except:
        return []


def get_password(username):
    try:
        rower = DBSession.query(Rower).filter_by(username=username).one()
        return rower.password
    except:
        return []
