from flask import Flask, request, jsonify, abort
from models import SessionLocal, StockData
from datetime import datetime

app = Flask(__name__)

@app.route('/stocks', methods=['GET'])
def get_all_stocks():
    """
    GET /stocks
    Retrieves all stock data from the StockData table.
    Optional query parameters:
      - name: filters records whose asset name contains the given substring.
      - sector_level1: filters by primary sector.
      - sector_level2: filters by secondary sector.
    """
    name = request.args.get('name')
    sector1 = request.args.get('sector_level1')
    sector2 = request.args.get('sector_level2')
    
    session = SessionLocal()
    query = session.query(StockData)
    
    if name:
        query = query.filter(StockData.name.ilike(f"%{name}%"))
    if sector1:
        query = query.filter(StockData.sector_level1 == sector1)
    if sector2:
        query = query.filter(StockData.sector_level2 == sector2)
    
    stocks = query.all()
    session.close()
    
    # Build a list of dictionaries representing each row.
    data = []
    for s in stocks:
        data.append({
            "id": s.id,
            "name": s.name,
            "asof": s.asof.isoformat(),
            "volume": s.volume,
            "close_usd": s.close_usd,
            "sector_level1": s.sector_level1,
            "sector_level2": s.sector_level2
        })
    return jsonify(data)

@app.route('/stocks/<string:asset_name>', methods=['GET'])
def get_stock_by_name(asset_name):
    """
    GET /stocks/<asset_name>
    Retrieves all daily records for the given asset name (exact match),
    ordered by date.
    """
    session = SessionLocal()
    stocks = session.query(StockData)\
        .filter(StockData.name == asset_name)\
        .order_by(StockData.asof)\
        .all()
    session.close()
    
    if not stocks:
        abort(404, description="Asset not found")
    
    data = []
    for s in stocks:
        data.append({
            "id": s.id,
            "name": s.name,
            "asof": s.asof.isoformat(),
            "volume": s.volume,
            "close_usd": s.close_usd,
            "sector_level1": s.sector_level1,
            "sector_level2": s.sector_level2
        })
    return jsonify(data)

@app.route('/stocks/<string:asset_name>/cumulative_returns', methods=['GET'])
def cumulative_returns(asset_name):
    """
    GET /stocks/<asset_name>/cumulative_returns?start=YYYY-MM-DD&end=YYYY-MM-DD
    Calculates the cumulative return for a given asset between two dates.
    The cumulative return is computed as: (end_price / start_price) - 1.
    """
    start_date_str = request.args.get('start')
    end_date_str = request.args.get('end')
    
    if not start_date_str or not end_date_str:
        abort(400, description="start and end dates are required in YYYY-MM-DD format")
    
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        abort(400, description="Dates must be in YYYY-MM-DD format")
    
    session = SessionLocal()
    # Get the earliest record on or after the start date for the asset.
    start_record = session.query(StockData)\
        .filter(StockData.name == asset_name, StockData.asof >= start_date)\
        .order_by(StockData.asof.asc())\
        .first()
    # Get the latest record on or before the end date for the asset.
    end_record = session.query(StockData)\
        .filter(StockData.name == asset_name, StockData.asof <= end_date)\
        .order_by(StockData.asof.desc())\
        .first()
    session.close()
    
    if not start_record or not end_record:
        abort(404, description="Price data not found for the given dates")
    
    start_price = start_record.close_usd
    end_price = end_record.close_usd
    cumulative_return = (end_price / start_price) - 1
    
    return jsonify({
        "asset_name": asset_name,
        "start_date": start_date_str,
        "end_date": end_date_str,
        "start_price": start_price,
        "end_price": end_price,
        "cumulative_return": cumulative_return
    })

if __name__ == '__main__':
    app.run(debug=True)
