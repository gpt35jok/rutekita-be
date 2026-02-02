from extensions import db
from sqlalchemy import text
import time

def dijkstra_route(start_lon, start_lat, end_lon, end_lat):
    start_time = time.time()

    result = db.session.execute(
        text("""
            SELECT * FROM pgr_dijkstra(
               'SELECT gid AS id, source, target, cost FROM ways',
                (
                    SELECT id FROM ways_vertices_pgr
                    ORDER BY the_geom <-> ST_SetSRID(ST_Point(:start_lon, :start_lat), 4326)
                    LIMIT 1
                ),
                (
                    SELECT id FROM ways_vertices_pgr
                    ORDER BY the_geom <-> ST_SetSRID(ST_Point(:end_lon, :end_lat), 4326)
                    LIMIT 1
                ),
                directed := false
            );
        """),
        {
            "start_lon": start_lon,
            "start_lat": start_lat,
            "end_lon": end_lon,
            "end_lat": end_lat
        }
    ).fetchall()

    exec_time = time.time() - start_time

    return {
            "status": "success",
            "execution_time": exec_time,
            "path_nodes": len(result),
            "route": [
                {
                    "seq": row[0],      # Urutan langkah
                    "node": row[1],     # ID Titik (Vertex)
                    "edge": row[2],     # ID Jalan (GID dari tabel ways)
                    "cost": row[3],     # Beban/Jarak di ruas ini
                    "agg_cost": row[4]  # Total biaya sampai titik ini
                } for row in result
            ]
        }
