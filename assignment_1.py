"""
Assignment 1:
Single request processing blocking queue which is thread safe and has 1 producer and 5 consumers.
DO NOT use standard or built-in Java/Python library packages. 
Implement your own blocking queue. Make sure to handle edge cases.
Your submission should show how the processing from the extra consumers is blocked when the producer is producing at capacity.
"""

import threading
consumer_count = 5

class BlockingQueue:
    def __init__(self, max_size):
        self.max_size = max_size
        self.queue = []
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def put(self, item):
        """
        This function is to add items in queue.
        This should wait if the queue is not empty.

        """
        with self.not_full:
            while len(self.queue) >= self.max_size:
                print(f"Queue is full. Producer is waiting to add item...")
                self.not_full.wait()
            self.queue.append(item)
            self.not_empty.notify()
            print(f"Item {item} added to the queue.")

    def get(self):
        with self.not_empty:
            while not self.queue:
                print(f"Queue is empty. Consumer is waiting for item...")
                self.not_empty.wait()  
            item = self.queue.pop(0)
            self.not_full.notify()
            print(f"Item {item} retrieved from the queue.")
            return item


def producer(queue):
    for i in range(10):
        print(f"Producer is now producing item {i}")
        queue.put(i)


def consumer(queue, consumer_id):
    while True:
        item = queue.get()
        print(f"Consumer {consumer_id} is processing item {item}")


if __name__ == "__main__":
    print('Starting execution')
    filename = "assignment_1"
    queue = BlockingQueue(max_size=consumer_count)
    producer_thread = threading.Thread(target=producer, args=(queue,))
    consumer_threads = [threading.Thread(target=consumer, args=(queue, i)) for i in range(consumer_count)]

    producer_thread.start()
    for thread in consumer_threads:
        thread.start()

    producer_thread.join()
    for thread in consumer_threads:
        thread.join()
