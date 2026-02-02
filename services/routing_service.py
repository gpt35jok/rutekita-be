from extensions import db
from sqlalchemy import text
import time

def dijkstra_route(start_lon, start_lat, end_lon, end_lat):
    start_time = time.time()

    # Query ini menggabungkan hasil dijkstra dengan tabel ways untuk ambil Geometri & Nama
    result = db.session.execute(
        text("""
            SELECT 
                res.seq, 
                res.node, 
                res.edge, 
                res.cost, 
                res.agg_cost,
                w.name, 
                ST_AsGeoJSON(w.the_geom)::json as geometry
            FROM pgr_dijkstra(
                'SELECT gid AS id, source, target, cost FROM ways',
                (SELECT id FROM ways_vertices_pgr ORDER BY the_geom <-> ST_SetSRID(ST_Point(:start_lon, :start_lat), 4326) LIMIT 1),
                (SELECT id FROM ways_vertices_pgr ORDER BY the_geom <-> ST_SetSRID(ST_Point(:end_lon, :end_lat), 4326) LIMIT 1),
                directed := false
            ) AS res
            LEFT JOIN ways w ON res.edge = w.gid
            ORDER BY res.seq;
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
                "seq": row[0],
                "node": row[1],
                "edge": row[2],
                "cost": row[3],
                "agg_cost": row[4],
                "street_name": row[5] if row[5] else "Unnamed Road",
                "geometry": row[6]  # Ini yang akan dipakai Frontend untuk gambar garis
            } for row in result
        ]
    }