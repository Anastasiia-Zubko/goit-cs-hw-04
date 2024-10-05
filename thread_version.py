import os
import threading
from queue import Queue
import time

def search_keywords_in_file(file_path, keywords, result_queue):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    result_queue.put((keyword, file_path))
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_files_threading(file_paths, keywords, num_threads=4):
    result_queue = Queue()
    threads = []
    for i in range(num_threads):
        files_subset = file_paths[i::num_threads]
        thread = threading.Thread(target=process_subset, args=(files_subset, keywords, result_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    result_dict = {}
    while not result_queue.empty():
        keyword, file_path = result_queue.get()
        if keyword not in result_dict:
            result_dict[keyword] = []
        result_dict[keyword].append(file_path)

    return result_dict

def process_subset(file_paths, keywords, result_queue):
    for file_path in file_paths:
        search_keywords_in_file(file_path, keywords, result_queue)

if __name__ == "__main__":
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']  
    keywords = ['test1', 'test2']  

    start_time = time.time()
    result = process_files_threading(files, keywords)
    end_time = time.time()

    print(f"Results for threading: {result}")
    print(f"Time taken for threading: {end_time - start_time} seconds")
