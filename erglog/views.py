from pyramid.response import Response
from pyramid.httpexceptions import(
    HTTPFound,
    HTTPNotFound,
    )
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Rower,
    ErgRecord
    )

import datetime

@view_config(route_name='home', renderer='templates/home.pt')
def home_page(request):

    rower_list = DBSession.query(Rower).all()

    if 'form.rower_added' in request.params:
        # Adding a rower
        rower_name = request.params['rower_name']
        rower = Rower(rower_name)
        try:
            DBSession.add(rower)
            message='Added new rower: ' + rower_name + '. Thankyou.'
        except DBAPIError:
            message='Failed to add new rower. Sorry.'

    elif 'form.ergrecord_added' in request.params:
        # Adding an erg record
        rower_id = request.params['rower_id']
        rower = DBSession.query(Rower).filter_by(id=rower_id).one()
        date = datetime.datetime.strptime(request.params['ergrecord_date'], '%Y-%m-%d')
        distance = int(request.params['ergrecord_distance'])
        ergrecord = ErgRecord(rower_id, date, distance)
        try:
            DBSession.add(ergrecord)
            message='Added new erg record: '+ rower.name + ' rowed ' + str(distance) + 'm in 30 minutes. Thankyou.'
        except DBAPIError:
            message='Failed to add new erg record. Sorry.'

    elif 'form.display_requested' in request.params:
        # Table or graph requested
        rower_id = request.params['rower_id']
        display_type = request.params['display_type']
        return HTTPFound(location = request.route_url(display_type,rower_id=rower_id))

    else:
        # Otherwise return default
        message='Welcome to ErgLog. Enjoy your stay.'

    return dict(message=message, rower_list=rower_list)



@view_config(route_name='table', renderer='templates/table.pt')
def erg_table(request):
    # Make a list of ergs to display
    rower_id = int(request.matchdict['rower_id'])
    if rower_id == 0:
        erg_list = DBSession.query(ErgRecord).all()
    else:
        erg_list = DBSession.query(ErgRecord).filter_by(rower_id=rower_id).all()

    # If there aren't any, 404 it
    if not erg_list:
        return HTTPNotFound('No such page')
    entries = []
    
    # Sort and convert to text
    erg_list.sort(key=lambda erg: erg.date)
    for erg in erg_list:
        date = datetime.datetime.strftime(erg.date,'%Y-%m-%d')
        rower = DBSession.query(Rower).filter_by(id=erg.rower_id).one().name
        distance = str(erg.distance)
        split = str(erg.split)
        entry = {"date":date, "rower":rower, "distance":distance, "split":split}
        entries.append(entry)

    return {"entries":entries}


@view_config(route_name='graph', renderer='templates/graph.pt')
def erg_graph(request):
    return HTTPNotFound('No such page')
