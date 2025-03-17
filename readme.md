# Benchmark IO with Binance

This repository contains the **Benchmark IO with Binance** project, designed to perform network and file I/O benchmarking. The project uses Python and various libraries to collect, process, and log benchmarking data.

## **Table of Contents**
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Functions](#functions)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## **Installation**

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/benchmark-io-with-binance.git
   cd benchmark-io-with-binance
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Rename `example.env` to `.env` and set the variables as per your needs.
   ```sh
   cp example.env .env
   ```

---

## **Usage**

### **In Development:**
Run the following command:
```sh
python benchmark_io.py
```

### **Using Docker:**

1. **Build the Docker image:**
   ```sh
   docker build -t benchmark-io .
   ```

2. **Run the Docker container:**
   ```sh
   docker run -d --name benchmark-io-container benchmark-io
   ```

---

## **Environment Variables**

Set the following environment variables in your `.env` file:

```ini
SERVER_ID=your_server_id
SERVER_IP=your_server_ip
NUM_RUNS=20
DELAY_BETWEEN_RUNS=0
JOB_SCHEDULE="15:22"
LOG_API_BASE=https://log-api.hassankhurram.com/log
MAX_WORKERS=50
```

---

## **Functions**

### **`execute_benchmark`**
The main function of the project that performs network and file I/O benchmarking tasks.

### **`log_event`**
Logs events to the log API using GET requests in a non-blocking way.

### **`benchmark_binance_data_pull`**
Performs network I/O benchmarking by pulling data from Binance.

### **`benchmark_file_io`**
Performs file I/O benchmarking by reading and writing files.

---

## **License**
This project is licensed under the **MIT License** – see the `LICENSE.md` file for details.

---

## **Acknowledgments**
This project was inspired by the following resources:
- Python
- Binance API
- APScheduler
- psutil

Feel free to contact me at **support@hassankhurram.com** if you have any questions or suggestions. You can also raise an issue if needed.
