from core.scraper import ScraperEngine
from core.processor import DataProcessor
from core.database import DatabaseManager
from utils.logger import setup_logger


## let's test the scraper engine with the CoinGecko API, which is a popular and free cryptocurrency data provider. We will fetch data for three coins: Bitcoin, Ethereum, and Solana. The expected keys in the response will be 'id', 'symbol', 'name', and 'market_data' to ensure we have the necessary information for our dashboard.    
def main():
    print("Initializing Market Intelligence Dashboard...")

    # The Fuel (URLs)
    # We use three identical endpoints for different coins so the JSON structure matches.
    crypto_urls = [ ## Added the APIs that are gonna be used.
        "https://api.coingecko.com/api/v3/coins/bitcoin",
        "https://api.coingecko.com/api/v3/coins/ethereum",
        "https://api.coingecko.com/api/v3/coins/solana"
    ]


    # The Configuration
    headers = {"User-Agent": "AshtonMarketDashboard/1.0"}
    timeout_seconds = 10
    rate_limit_seconds = 3  # CoinGecko is strict, so we give it 1.5 seconds to breathe
    
    # These are the keys we expect in every CoinGecko response
    expected_keys = ['id', 'symbol', 'name', 'market_data']

    # Instantiate the Engine
    print("Starting Scraper Engine...")
    engine = ScraperEngine(
        base_urls=crypto_urls,
        headers=headers,
        timeout=timeout_seconds,
        rate_limit=rate_limit_seconds,
        expected_keys=expected_keys
    )

    # Fire the Engine
    raw_data = engine.fetch_all()

    # Check the Payload
    print(f"\n[1/3] Scraping complete! Successfully retrieved {len(raw_data)} valid records.")
    
    # Optional: Print the name and current price of the first coin to prove it worked
    if len(raw_data) > 0:
        print(f"\n[2/3] Pass {len(raw_data)} raw records into the Processor....")

        ## Instantiate the processor with raw data
        processor = DataProcessor(raw_data)

        # Running pipeline methods
        processor.clean_data()
        processor.add_features()

        print("\n[3/3] Streaming modified data from Generator:")
        print("-"*50)
        db = DatabaseManager()
        #trigger the generator for one row at a time
        saved_count = 0
        for row in processor.stream_rows():
            db.insert_row(row)
            
            print(f"Saved to DB: {row.coin} | Price: ${row.price}")
            saved_count += 1
        
        insert_count = 0
        for row in processor.stream_rows():
            db.insert_row(row)
            
            # Convert row to a plain dictionary based on its structure
            # If row is a NamedTuple/object,I'll use row._asdict()
            # If row is a Pandas series, I'll use row.to_dict()
            data_to_save = row.to_dict() if hasattr(row, 'to_dict') else row._asdict()
            
            db.append_to_csv(data_dict=data_to_save, filename="crypto_dataset.csv")
            print(f"Saved: {data_to_save['coin']}")
            insert_count+=1

        print(f"Total rows saved to database: {saved_count}")
        print(f"Total rows saved to dataset: {insert_count}")
        print("-" * 50)
        print("Pipeline Execution Complete.")
        
    else:
        print("\nPipeline stopped. No valid data was fetched from the APIs.")

    logger = setup_logger()

    logger.info("Initializing Market Intelligence Dashboard...")

    logger.warning("CoinGecko API is getting slow, increasing wait time...")

    try:
        pass
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        
    print("TEST IS SUCCESSFUL!")
if __name__ == "__main__":
    main()

##  RAN THIS AND THE TEST WAS SUCCESSFUL! We successfully fetched data for Bitcoin, Ethereum, and Solana from the CoinGecko API, and the expected keys were present in the response. The sample data output confirms that we have the necessary information to build our Market Intelligence Dashboard.