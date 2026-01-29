from extensions import db
import time
from sqlalchemy import text

def dijkstra_route(start_lon, start_lat, end_lon, end_lat):
    start_time = time.time()

    query = """
    SELECT * FROM pgr_dijkstra(
        'SELECT id, source, target, cost FROM ways',
        (
            SELECT id FROM ways_vertices_pgr
            ORDER BY the_geom <-> ST_SetSRID(ST_Point(%s, %s), 4326)
            LIMIT 1
        ),
        (
            SELECT id FROM ways_vertices_pgr
            ORDER BY the_geom <-> ST_SetSRID(ST_Point(%s, %s), 4326)
            LIMIT 1
        ),
        directed := false
    );
    """

    result = db.session.execute(
        text(query),
        {
            "start_lon": start_lon,
            "start_lat": start_lat,
            "end_lon": end_lon,
            "end_lat": end_lat
        }
    ).fetchall()

    exec_time = time.time() - start_time

    return {
        "execution_time": exec_time,
        "path_nodes": len(result)
    }
