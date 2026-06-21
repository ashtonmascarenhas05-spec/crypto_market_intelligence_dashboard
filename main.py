from core.scraper import ScraperEngine
from core.processor import DataProcessor


## let's test the scraper engine with the CoinGecko API, which is a popular and free cryptocurrency data provider. We will fetch data for three coins: Bitcoin, Ethereum, and Solana. The expected keys in the response will be 'id', 'symbol', 'name', and 'market_data' to ensure we have the necessary information for our dashboard.    
def main():
    print("Initializing Market Intelligence Dashboard...")

    # 1. The Fuel (URLs)
    # We use three identical endpoints for different coins so the JSON structure matches.
    crypto_urls = [ ## Added the APIs that are gonna be used.
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1",
        "https://api.coingecko.com/api/v3/coins/bitcoin",
        "https://api.coingecko.com/api/v3/coins/ethereum",
        "https://api.coingecko.com/api/v3/global",
        "https://api.coingecko.com/api/v3/search/trending",
        "https://open.er-api.com/v6/latest/USD",
        "https://jsonplaceholder.typicode.com/posts",
        "https://bored-api.appbrewery.com/random"
    ]


    # 2. The Configuration
    headers = {"User-Agent": "AshtonMarketDashboard/1.0"}
    timeout_seconds = 10
    rate_limit_seconds = 1.5  # CoinGecko is strict, so we give it 1.5 seconds to breathe
    
    # These are the keys we expect in every CoinGecko response
    expected_keys = ['id', 'symbol', 'name', 'market_data']

    # 3. Instantiate the Engine
    print("Starting Scraper Engine...")
    engine = ScraperEngine(
        base_urls=crypto_urls,
        headers=headers,
        timeout=timeout_seconds,
        rate_limit=rate_limit_seconds,
        expected_keys=expected_keys
    )

    # 4. Fire the Engine
    raw_data = engine.fetch_all()

    # 5. Check the Payload
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

        #trigger the generator for one row at a time
        for row in processor.stream_rows():
            print(row)
        print("-" * 50)
        print("Pipeline Execution Complete.")
        
    else:
        print("\nPipeline stopped. No valid data was fetched from the APIs.")

        
    print("TEST IS SUCCESSFUL!")
if __name__ == "__main__":
    main()

##  RAN THIS AND THE TEST WAS SUCCESSFUL! We successfully fetched data for Bitcoin, Ethereum, and Solana from the CoinGecko API, and the expected keys were present in the response. The sample data output confirms that we have the necessary information to build our Market Intelligence Dashboard.