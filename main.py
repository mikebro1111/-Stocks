import time
import os

# Main execution
from wiki_client import WikiClient, ThreadManager

if __name__ == "__main__":
    db_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    symbols = WikiClient.get_wiki_symbols()
    thread_manager = ThreadManager(symbols, db_url)

    start_time = time.time()
    thread_manager.execute_threads()
    end_time = time.time()

    execution_time = end_time - start_time
    seconds = execution_time
    minutes = seconds / 60

    print("Час виконання програми в секундах:", seconds)
    print("Час виконання програми в хвилинах:", minutes)
