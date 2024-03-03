n = int(input())

nums = map(int, input().split())

from collections import defaultdict

d = defaultdict(int)

for num in nums:
    d[num] += 1

max_val = max(d.values())

for k, v in d.items():
    if v == max_val:
        print(k)
        break