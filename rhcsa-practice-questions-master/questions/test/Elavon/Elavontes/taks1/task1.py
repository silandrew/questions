from flask import Flask, request, jsonify
import pymysql
import pymongo
import yaml
import datetime

app = Flask(__name__)

# Load configuration
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

db_config = config['database']

@app.route('/transactions', methods=['GET'])
def get_transactions():
    n_days = request.args.get('n_days', default=7, type=int)
    card_type = request.args.get('card_type')
    country_origin = request.args.get('country_origin')
    min_amount = request.args.get('min_amount', type=float)
    max_amount = request.args.get('max_amount', type=float)

    # Calculate date n days ago
    n_days_ago = datetime.datetime.now() - datetime.timedelta(days=n_days)
    
    if db_config['type'] == 'mysql':
        # MySQL connection
        conn = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            db=db_config['dbname']
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Building the SQL Query
        query = "SELECT * FROM transactions WHERE transaction_date >= %s"
        params = [n_days_ago]

        if card_type:
            query += " AND CardType = %s"
            params.append(card_type)
            
        if country_origin:
            query += " AND CountryOrigin = %s"
            params.append(country_origin)

        if min_amount is not None and max_amount is not None:
            query += " AND Amount BETWEEN %s AND %s"
            params.extend([min_amount, max_amount])
        
        # Executing the SQL Query
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Closing the connection
        cursor.close()
        conn.close()
    elif db_config['type'] == 'mongodb':
        # MongoDB connection
        client = pymongo.MongoClient(
            host=db_config['host'],
            port=db_config['port'],
            username=db_config['user'],
            password=db_config['password']
        )
        db = client[db_config['dbname']]
        collection = db['transactions']

        # Building the query
        query = {"transaction_date": {"$gte": n_days_ago}}
        if card_type:
            query["CardType"] = card_type
        if country_origin:
            query["CountryOrigin"] = country_origin
        if min_amount is not None and max_amount is not None:
            query["Amount"] = {"$gte": min_amount, "$lte": max_amount}
        
        # Executing the query
        results = list(collection.find(query))
    else:
        return jsonify({"error": "Invalid database type in config.yaml"}), 400
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
