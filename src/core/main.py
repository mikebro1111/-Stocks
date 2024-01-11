from dotenv import find_dotenv, load_dotenv
from wiki_client import WikiClient, ThreadManager
import time
import os

# Load environment variables from .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Retrieve MongoDB connection string and URL from environment variables
MONGO_CONNECTIONS = os.getenv("MONGO_CONNECTIONS")
URL = os.getenv("URL")

# Main execution block
if __name__ == "__main__":
    # Initialize database URL and symbols
    db_url = os.getenv("MONGO_URL", MONGO_CONNECTIONS)
    symbols = WikiClient.get_wiki_symbols(URL)

    # Create and execute ThreadManager
    thread_manager = ThreadManager(symbols, db_url)
    start_time = time.time()
    thread_manager.execute_threads()
    end_time = time.time()

    # Calculate and print the execution time
    execution_time = end_time - start_time
    seconds = execution_time
    minutes = seconds / 60
    print("Execution time in seconds:", seconds)
    print("Execution time in minutes:", minutes)
