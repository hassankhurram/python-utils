import time
import requests
import threading
import os
import sys
import datetime
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler  # Scheduler library with timezone support
from apscheduler.triggers.cron import CronTrigger
import pytz  # Timezone library
import psutil  # Library to get system information

# Replace with actual server ID when running on each server
SERVER_ID = '1'  # Change to '6' for server 6, and '1' for server 1

# Replace with the static, whitelisted IP address for each server
SERVER_IP = '192.0.2.1'  # Example IP for server 5
# For server 1: SERVER_IP = '192.0.2.1'
# For server 6: SERVER_IP = '192.0.2.6'

# Number of runs per job (default is 20)
NUM_RUNS = 20  # Adjust as needed

# Delay between runs in seconds (optional)
DELAY_BETWEEN_RUNS = 0  # Set to desired number of seconds

# Define the timezone
timezone = pytz.timezone('Asia/Karachi')

# Scheduler configuration
JOB_SCHEDULE = "15:22"  # Time to run the job daily (24-hour format HH:MM)

RUN_TAG = f"{JOB_SCHEDULE}-{NUM_RUNS}"

# Log API base endpoint
# you can comment out this section to save logs or just console. log it
LOG_API_BASE = 'https://openlogs.hassankhurram.com/log'

# Maximum number of threads for the thread pool
MAX_WORKERS = 50  # Adjust based on your needs and system resources

# Create a ThreadPoolExecutor for logging
log_executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

# Function to collect system metrics
def get_system_metrics():
    # Get CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Get memory usage
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent
    
    # Get disk usage
    
    # Return as a dictionary
    return {
        'cpu_percent': cpu_percent,
        'memory_percent': memory_percent,
    }

# Function to log events to the log API using GET requests in a non-blocking way
def log_event(server_id, event_name, params=None):
    if params is None:
        params = {}

    

    url = f'{LOG_API_BASE}/{RUN_TAG}/{server_id}/{event_name}'

    def send_log_request():
        try:
            # Get system metrics and add them to the event log
            system_metrics = get_system_metrics()
            params.update(system_metrics)
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to log event: {e}")

    # Submit the log request to the thread pool executor
    log_executor.submit(send_log_request)

# Function to perform network I/O benchmarking
def benchmark_binance_data_pull(run_number):
    network_start_time = time.time()
    # Log event before network calls
    log_event(
        server_id=SERVER_ID,
        event_name='NETWORK_CALL_START',
        params={
            'timestamp': network_start_time,
            'run_number': run_number
        }
    )
    try:
        # Fetch latest price for multiple symbols
        symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT']
        for symbol in symbols:
            symbol_start_time = time.time()
            # Log event before each individual network call
            log_event(
                server_id=SERVER_ID,
                event_name='NETWORK_CALL_SYMBOL_START',
                params={
                    'timestamp': symbol_start_time,
                    'run_number': run_number,
                    'symbol': symbol
                }
            )

            url = 'https://api.binance.com/api/v3/ticker/price'
            params = {'symbol': symbol}
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                print(f"Symbol: {data['symbol']}, Price: {data['price']}")
            except Exception as e:
                print(f"Failed to fetch data for symbol {symbol}: {e}")

            symbol_end_time = time.time()
            symbol_duration = symbol_end_time - symbol_start_time

            # Log event after each individual network call
            log_event(
                server_id=SERVER_ID,
                event_name='NETWORK_CALL_SYMBOL_END',
                params={
                    'timestamp': symbol_end_time,
                    'run_number': run_number,
                    'symbol': symbol,
                    'duration': symbol_duration
                }
            )
    except Exception as e:
        print(f"Binance data pull failed: {e}")
    network_end_time = time.time()
    total_network_duration = network_end_time - network_start_time
    # Log event after network calls
    log_event(
        server_id=SERVER_ID,
        event_name='NETWORK_CALL_END',
        params={
            'timestamp': network_end_time,
            'run_number': run_number,
            'total_duration': total_network_duration
        }
    )
    return total_network_duration

# Function to perform file I/O benchmarking
def benchmark_file_io(temp_dir_path, run_number):
    file_start_time = time.time()
    # Log event before file operations
    log_event(
        server_id=SERVER_ID,
        event_name='FILE_IO_START',
        params={
            'timestamp': file_start_time,
            'run_number': run_number
        }
    )

    test_filename = os.path.join(temp_dir_path, f'io_test_file_{run_number}.tmp')
    # Approx 2.1 MB of data
    test_data = 'This is a test.' * 1000  

    try:
        # Log event before writing the file
        write_start_time = time.time()
        log_event(
            server_id=SERVER_ID,
            event_name='FILE_WRITE_START',
            params={
                'timestamp': write_start_time,
                'run_number': run_number,
                'filename': test_filename
            }
        )

        # Write test data to a file
        with open(test_filename, 'w') as f:
            f.write(test_data)

        write_end_time = time.time()
        write_duration = write_end_time - write_start_time

        # Log event after writing the file
        log_event(
            server_id=SERVER_ID,
            event_name='FILE_WRITE_END',
            params={
                'timestamp': write_end_time,
                'run_number': run_number,
                'filename': test_filename,
                'duration': write_duration
            }
        )

        # Log event before reading the file
        read_start_time = time.time()
        log_event(
            server_id=SERVER_ID,
            event_name='FILE_READ_START',
            params={
                'timestamp': read_start_time,
                'run_number': run_number,
                'filename': test_filename
            }
        )

        # Read the data back
        with open(test_filename, 'r') as f:
            _ = f.read()

        read_end_time = time.time()
        read_duration = read_end_time - read_start_time

        # Log event after reading the file
        log_event(
            server_id=SERVER_ID,
            event_name='FILE_READ_END',
            params={
                'timestamp': read_end_time,
                'run_number': run_number,
                'filename': test_filename,
                'duration': read_duration
            }
        )

    except Exception as e:
        print(f"File I/O operation failed: {e}")
    file_end_time = time.time()
    file_duration = file_end_time - file_start_time

    # Log event after file operations
    log_event(
        server_id=SERVER_ID,
        event_name='FILE_IO_END',
        params={
            'timestamp': file_end_time,
            'run_number': run_number,
            'total_duration': file_duration
        }
    )

    return file_duration

# Function to execute the benchmarking tasks
def execute_benchmark():
    
    log_event(
        server_id=SERVER_ID,
        event_name='CRON_START',
        params={
            'timestamp': time.time(),
            'ip': SERVER_IP,
            "run_tag": RUN_TAG
        }
    )
    
    # Create temp directory
    temp_dir_name = f'temp_io_files_{int(time.time())}_{SERVER_ID}'
    temp_dir_path = os.path.join(os.getcwd(), temp_dir_name);
    try:
        os.makedirs(temp_dir_path)
        print(f"Created temp directory at {temp_dir_path}")
    except Exception as e:
        print(f"Failed to create temp directory: {e}")
        return  # Exit if temp directory cannot be created

    for run_number in range(1, NUM_RUNS + 1):
        print(f"\nStarting run {run_number}/{NUM_RUNS} at {datetime.datetime.now()}")
        total_start_time = time.time()

        # Log start event using GET request in a non-blocking way
        log_event(
            server_id=SERVER_ID,
            event_name='RUN_START',
            params={
                'timestamp': total_start_time,
                'ip': SERVER_IP,
                'run_number': run_number
            }
        )

        # Perform network I/O benchmarking
        network_duration = benchmark_binance_data_pull(run_number)
        print(f"Network I/O duration: {network_duration:.2f} seconds")

        # Perform file I/O benchmarking
        file_duration = benchmark_file_io(temp_dir_path, run_number)
        print(f"File I/O duration: {file_duration:.2f} seconds")

        total_end_time = time.time()
        total_duration = total_end_time - total_start_time

        # Log end event using GET request in a non-blocking way
        log_event(
            server_id=SERVER_ID,
            event_name='RUN_END',
            params={
                'timestamp': total_end_time,
                'total_duration_seconds': total_duration,
                'network_io_duration_seconds': network_duration,
                'file_io_duration_seconds': file_duration,
                'ip': SERVER_IP,
                'run_number': run_number
            }
        )

        # Print results for verification
        print(f"Run {run_number} completed in {total_duration:.2f} seconds on server {SERVER_ID}.")

        # Delay between runs if specified
        if DELAY_BETWEEN_RUNS > 0 and run_number < NUM_RUNS:
            print(f"Waiting {DELAY_BETWEEN_RUNS} seconds before next run...")
            time.sleep(DELAY_BETWEEN_RUNS)

    # Clean up temp directory after all runs
    try:
        for filename in os.listdir(temp_dir_path):
            file_path = os.path.join(temp_dir_path, filename)
            os.remove(file_path)
        os.rmdir(temp_dir_path)
        print(f"Deleted temp directory at {temp_dir_path}")
    except Exception as e:
        print(f"Failed to delete temp directory: {e}")
        
    log_event(
        server_id=SERVER_ID,
        event_name='CRON_END',
        params={
            'timestamp': time.time(),
            'ip': SERVER_IP,
            "run_tag": RUN_TAG
        }
    )

# Main function
def main():
    scheduler = BlockingScheduler()

    # Schedule the job
    # JOB_SCHEDULE is in format 'HH:MM'
    hour, minute = map(int, JOB_SCHEDULE.split(':'))
    scheduler.add_job(execute_benchmark, CronTrigger(hour=hour, minute=minute, timezone=timezone))

    print(f"Scheduler started. Benchmark will run at {JOB_SCHEDULE} PKT.")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Scheduler stopped by user.")
    finally:
        # Clean up the thread pool executor
        log_executor.shutdown(wait=False)
        print("Log executor shut down.")

if __name__ == '__main__':
    # Allow setting number of runs and server ID via command-line argument (optional)
    if len(sys.argv) > 1:
        try:
            NUM_RUNS = int(sys.argv[1])
            SERVER_ID = str(sys.argv[2])  # Keep SERVER_ID as a string
            RUN_TAG = f"{JOB_SCHEDULE}-{NUM_RUNS}"
            print(f"Number of runs set to {NUM_RUNS} and Server ID set to {SERVER_ID} via command-line argument.")
        except ValueError:
            print("Invalid number of runs or server ID specified. Using default values.")

    main()
