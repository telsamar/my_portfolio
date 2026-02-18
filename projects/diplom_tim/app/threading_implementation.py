import requests
import time
import psutil
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import random

def safe_del(self):
    pass

if hasattr(threading, '_DeleteDummyThreadOnDel'):
    threading._DeleteDummyThreadOnDel.__del__ = safe_del

RESULTS_FILE = 'app/threading_results.json'
API_URL = 'http://universities.hipolabs.com/search?country=Russian+Federation'
NUM_REQUESTS = 100
MAX_THREADS = 10

successful_requests = 0
failed_requests = 0
lock = threading.Lock()

def fetch_universities(request_number, max_retries=3):
    global successful_requests, failed_requests
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()
            with lock:
                successful_requests += 1
            print(f"Запрос {request_number}/{NUM_REQUESTS} выполнен.")
            return True
        except requests.RequestException as e:
            print(f"Ошибка при запросе {request_number} (попытка {attempt}): {e}")
            if attempt < max_retries:
                sleep_time = 2 ** attempt + random.uniform(0, 1)
                print(f"Повторная попытка через {sleep_time:.2f} секунд...")
                time.sleep(sleep_time)
    with lock:
        failed_requests += 1
    print(f"Запрос {request_number}/{NUM_REQUESTS} не удался после {max_retries} попыток.")
    return False

def perform_test():
    global successful_requests, failed_requests
    results = {
        'total_requests': NUM_REQUESTS,
        'successful_requests': 0,
        'failed_requests': 0,
        'average_time_per_request': 0.0,
        'cpu_usage_percent': 0.0,
        'memory_usage_mb': 0.0,
        'total_elapsed_time': 0.0
    }

    process = psutil.Process(os.getpid())
    cpu_times_before = process.cpu_times()
    total_cpu_time_before = cpu_times_before.user + cpu_times_before.system
    mem_before = process.memory_info().rss / (1024 * 1024)

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(fetch_universities, i + 1) for i in range(NUM_REQUESTS)]
        for future in as_completed(futures):
            pass
        executor.shutdown(wait=True)

    end_time = time.time()

    cpu_times_after = process.cpu_times()
    total_cpu_time_after = cpu_times_after.user + cpu_times_after.system
    mem_after = process.memory_info().rss / (1024 * 1024)

    delta_cpu_time = total_cpu_time_after - total_cpu_time_before
    delta_wall_time = end_time - start_time
    cpu_usage_percent = (delta_cpu_time / delta_wall_time) * 100

    results['successful_requests'] = successful_requests
    results['failed_requests'] = failed_requests
    results['total_elapsed_time'] = delta_wall_time
    results['average_time_per_request'] = delta_wall_time / NUM_REQUESTS
    results['cpu_usage_percent'] = cpu_usage_percent
    results['memory_usage_mb'] = mem_after - mem_before

    return results

def save_results(results):
    try:
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"Результаты тестирования сохранены в файл {RESULTS_FILE}.")
    except IOError as e:
        print(f"Ошибка при сохранении результатов: {e}")

def main():
    print("Начало многопоточного тестирования с использованием ThreadPoolExecutor...")
    results = perform_test()
    print("Тестирование завершено.")
    print(json.dumps(results, indent=4, ensure_ascii=False))
    save_results(results)

if __name__ == "__main__":
    main()
