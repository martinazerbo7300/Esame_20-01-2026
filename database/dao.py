from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def artisti_by_min_albums(n_alb):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        artisti_min_albums = []
        query = """
            SELECT a.id, COUNT(al.title) as n_alb
            FROM artist a, album al
            WHERE a.id = al.artist_id
            GROUP BY a.id
            HAVING n_alb >= %s
            """

        cursor.execute(query, (n_alb,))
        for row in cursor:
            artisti_min_albums.append(row['n_alb'])

        cursor.close()
        conn.close()

        return artisti_min_albums

    @staticmethod
    def get_artist_genre_map(artists):
        conn = DBConnect.get_connection()
        result = {a: set() for a in artists}
        artist_ids = tuple(a.id for a in artists)
        if not artist_ids:
            return result

        cursor = conn.cursor(dictionary=True)
        query = f"""
                       SELECT t.genre_id , g.id
                    FROM track t, genre g
                    WHERE genre_id = t.genre_id  and t.genre IN {artist_ids}
                    """
        cursor.execute(query)
        for row in cursor:
            artist = next((a for a in artists if a.id == row['genre_id']), None)
            if artist:
                result[artist].add(row['genre_id'])
        cursor.close()
        conn.close()
        return result
