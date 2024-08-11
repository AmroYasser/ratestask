from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
from datetime import datetime

app = Flask(__name__)

def get_ports_from_region(region_slug, cur):
    query = """
    WITH RECURSIVE region_tree AS (
        SELECT slug FROM regions WHERE slug = %s
        UNION ALL
        SELECT r.slug FROM regions r
        INNER JOIN region_tree rt ON rt.slug = r.parent_slug
    )
    SELECT p.code FROM ports p
    INNER JOIN region_tree rt ON rt.slug = p.parent_slug;
    """
    cur.execute(query, (region_slug,))
    return [row[0] for row in cur.fetchall()]

def check_existence(items, cur):
    if not items:
        return False
    query = """
    SELECT EXISTS(
        SELECT 1 FROM ports WHERE code = ANY(%s)
        UNION ALL
        SELECT 1 FROM regions WHERE slug = ANY(%s)
    );
    """
    cur.execute(query, (items, items))
    return cur.fetchone()[0]

def validate_date(date_str):
    """Validate the date format to be YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


@app.route('/rates', methods=['GET'])
def get_rates():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    # Validate dates
    if not validate_date(date_from) or not validate_date(date_to):
        return jsonify({"error": "Invalid date format, please use YYYY-MM-DD"}), 400

    conn = psycopg2.connect("dbname=postgres user=postgres password=ratestask host=db")
    cur = conn.cursor()

    try:
        # Determine origin/destination ports: If the origin/destination string length exceeds 5 characters, assume it's a region slug
        # and fetch all associated port codes. Otherwise, treat it as a single port code.
        origin_ports = get_ports_from_region(origin, cur) if len(origin) > 5 else [origin]
        destination_ports = get_ports_from_region(destination, cur) if len(destination) > 5 else [destination]

        # Check existence of origin and destination
        if not check_existence(origin_ports, cur) or not check_existence(destination_ports, cur):
            return jsonify({"error": "Origin or destination does not exist"}), 404

        query = """
       SELECT day, 
               CASE 
                   WHEN COUNT(price) >= 3 THEN AVG(price)
                   ELSE NULL
               END AS average_price
        FROM prices
        WHERE orig_code = ANY(%s) AND dest_code = ANY(%s)
          AND day BETWEEN %s AND %s
        GROUP BY day
        """
        cur.execute(query, (origin_ports, destination_ports, date_from, date_to))

        results = cur.fetchall()
        result_list = [{"day": result[0], "average_price": result[1]} for result in results]
        return jsonify(result_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)