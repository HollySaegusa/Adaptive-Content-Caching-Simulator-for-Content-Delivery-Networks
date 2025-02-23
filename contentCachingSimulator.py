import random
import time
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.freq = {}

    def get(self, key):
        if key in self.cache:
            self.freq[key] += 1
            return self.cache[key]
        return -1

    def put(self, key, value):
        if self.capacity <= 0:
            return

        if key in self.cache:
            self.freq[key] += 1
        elif len(self.cache) >= self.capacity:
            lfu_key = min(self.freq, key=self.freq.get)
            self.cache.pop(lfu_key)
            self.freq.pop(lfu_key)
            self.freq[key] = 1
        else:
            self.freq[key] = 1
        self.cache[key] = value

class AdaptiveTTLCache:
    def __init__(self, capacity, base_ttl):
        self.capacity = capacity
        self.cache = {}
        self.expiry = {}
        self.base_ttl = base_ttl

    def get(self, key):
        current_time = time.time()
        if key in self.cache and self.expiry[key] > current_time:
            return self.cache[key]
        elif key in self.cache:
            del self.cache[key]
            del self.expiry[key]
        return -1

    def put(self, key, value):
        current_time = time.time()
        if len(self.cache) >= self.capacity:
            to_remove = min(self.expiry, key=self.expiry.get)
            del self.cache[to_remove]
            del self.expiry[to_remove]
        ttl = self.base_ttl + random.randint(0, 10)
        self.cache[key] = value
        self.expiry[key] = current_time + ttl

class ContentRequestSimulator:
    def __init__(self, num_requests, cache, use_zipf=False):
        self.num_requests = num_requests
        self.cache = cache
        self.use_zipf = use_zipf
        self.content_ids = list(range(1, 101))

    def generate_request(self):
        if self.use_zipf:
            weights = np.random.zipf(a=2.0, size=len(self.content_ids))
            probabilities = weights / sum(weights)
            return np.random.choice(self.content_ids, p=probabilities)
        return random.randint(1, 100)

    def run_simulation(self):
        hit_count = 0
        start_time = time.time()
        for i in range(self.num_requests):
            content_id = self.generate_request()
            if self.cache.get(content_id) != -1:
                hit_count += 1
            else:
                self.cache.put(content_id, f"Content {content_id}")
        end_time = time.time()
        avg_response_time = (end_time - start_time) / self.num_requests
        return hit_count / self.num_requests, avg_response_time

if __name__ == "__main__":
    num_requests = 1000
    initial_cache_capacity = 50

    results = {}
    response_times = {}

    for capacity_factor in [1.0, 1.5, 2.0]:
        print(f"\nSimulating with Cache Capacity: {int(initial_cache_capacity * capacity_factor)}")

        dynamic_cache_capacity = int(initial_cache_capacity * capacity_factor)

        print("Simulating LRU Cache...")
        lru_cache = LRUCache(dynamic_cache_capacity)
        simulator = ContentRequestSimulator(num_requests, lru_cache, use_zipf=True)
        lru_hit_rate, lru_response_time = simulator.run_simulation()
        results[f'LRU-{capacity_factor}x'] = lru_hit_rate
        response_times[f'LRU-{capacity_factor}x'] = lru_response_time
        print(f"LRU Cache Hit Rate: {lru_hit_rate:.2%}, Avg Response Time: {lru_response_time:.5f} seconds")

        print("\nSimulating LFU Cache...")
        lfu_cache = LFUCache(dynamic_cache_capacity)
        simulator = ContentRequestSimulator(num_requests, lfu_cache, use_zipf=True)
        lfu_hit_rate, lfu_response_time = simulator.run_simulation()
        results[f'LFU-{capacity_factor}x'] = lfu_hit_rate
        response_times[f'LFU-{capacity_factor}x'] = lfu_response_time
        print(f"LFU Cache Hit Rate: {lfu_hit_rate:.2%}, Avg Response Time: {lfu_response_time:.5f} seconds")

        print("\nSimulating Adaptive TTL Cache...")
        adaptive_cache = AdaptiveTTLCache(dynamic_cache_capacity, base_ttl=5)
        simulator = ContentRequestSimulator(num_requests, adaptive_cache, use_zipf=True)
        adaptive_hit_rate, adaptive_response_time = simulator.run_simulation()
        results[f'Adaptive TTL-{capacity_factor}x'] = adaptive_hit_rate
        response_times[f'Adaptive TTL-{capacity_factor}x'] = adaptive_response_time
        print(f"Adaptive TTL Cache Hit Rate: {adaptive_hit_rate:.2%}, Avg Response Time: {adaptive_response_time:.5f} seconds")

    # Visualization
    fig, ax1 = plt.subplots()

    bar_positions = range(len(results))
    ax1.bar(bar_positions, [rate * 100 for rate in results.values()], color=['blue', 'orange', 'green', 'cyan', 'magenta', 'yellow'], alpha=0.7, label='Hit Rate (%)')
    ax1.set_ylabel('Hit Rate (%)')
    ax1.set_ylim(0, 100)
    ax1.set_xlabel('Cache Strategy and Capacity')
    ax1.set_xticks(bar_positions)
    ax1.set_xticklabels(results.keys(), rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(bar_positions, list(response_times.values()), color='red', marker='o', label='Avg Response Time (s)')
    ax2.set_ylabel('Avg Response Time (s)')

    fig.suptitle('Cache Strategy Performance with Zipf Distribution and Dynamic Capacities')
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))

    plt.tight_layout()
    plt.show()
