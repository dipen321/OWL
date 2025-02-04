import csv
from datetime import datetime
from models import get_engine, create_tables, StockData, SessionLocal

CSV_FILE = 'stock_data.csv'

def run_etl():
    # Create the database tables if they do not exist.
    engine = get_engine()
    create_tables(engine)
    
    # Create a new session for ORM operations.
    session = SessionLocal()
    
    # Open and read the CSV file.
    with open(CSV_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile) 
        for row in reader:
            # Parse and clean data from the CSV row.
            name = row['name'].strip()
            asof_str = row['asof'].strip()
            # Convert the asof date from string to a date object.
            asof_date = datetime.strptime(asof_str, "%Y-%m-%d").date()
            volume = int(row['volume'].strip())
            close_usd = float(row['close_usd'].strip())
            sector_level1 = row['sector_level1'].strip()
            sector_level2 = row['sector_level2'].strip()
            
            # Check if a record with the same asset name and date already exists.
            record = session.query(StockData).filter(
                StockData.name == name,
                StockData.asof == asof_date
            ).first()
            
            if not record:
                # If no record exists, create a new one.
                record = StockData(
                    name=name,
                    asof=asof_date,
                    volume=volume,
                    close_usd=close_usd,
                    sector_level1=sector_level1,
                    sector_level2=sector_level2
                )
                session.add(record)
            else:
                # Otherwise, update the existing record.
                record.volume = volume
                record.close_usd = close_usd
                record.sector_level1 = sector_level1
                record.sector_level2 = sector_level2
        
        session.commit()
    session.close()
    print("ETL completed successfully.")

if __name__ == '__main__':
    run_etl()
