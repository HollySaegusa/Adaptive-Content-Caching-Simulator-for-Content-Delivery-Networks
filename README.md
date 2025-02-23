System Architecture: 

Content Request Generator: This module generates a stream of content requests to simulate user access patterns. The request stream includes popular and less popular content to represent real-world traffic patterns.

Cache Module: Multiple caching strategies will be implemented, including LRU (Least Recently Used), LFU (Least Frequently Used), and Adaptive TTL. Each algorithm will be implemented as a separate class, making it easier to compare their performance.

Performance Monitoring and Logging: The simulator will log each content request’s result (hit or miss) and calculate metrics such as cache hit rate, miss rate, and average response time.

Implementation of Caching Strategies:

LRU Cache: This cache strategy will use an ordered dictionary to implement LRU by removing the least recently accessed items.

LFU Cache: This cache will track each item’s access frequency and remove the least frequently accessed items.

Adaptive TTL Cache: Based on access frequency and time, this cache dynamically adjusts the expiration time of items, keeping frequently accessed content cached longer.

![image](https://github.com/user-attachments/assets/c2ff956b-667e-48e3-95d2-13e17691a164)
