import psycopg2

conn = None

def initialize_db():
    global conn
    conn = psycopg2.connect(dbname="postgres",
                            host="localhost",
                            user="postgres",
                            password="123456789",
                            port=5432)

    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id SERIAL PRIMARY KEY,
        long_url TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()


def insert_db(long_url):
    global conn
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO urls (long_url) VALUES (%s) RETURNING id;
        """, (long_url,))
    insert_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    return insert_id

def redirect_lookup(serial_id):
    global conn
    cur = conn.cursor()
    cur.execute("""
        SELECT long_url FROM urls WHERE id = %s;
        """ , (serial_id,))
    
    long_url = cur.fetchone()[0]
    return long_url

def close_db():
    conn.close()
