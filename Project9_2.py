import threading

ranges = [
    [10, 20],
    [1, 5],
    [70, 80],
    [27, 92],
    [0, 16]
]

def range_sum(sum, i, start, end):
    sum[i] = 0
    end += 1
    sum[i] = end*(end-1)//2
    sum[i] -= start*(start-1)//2
    #for j in range(start, end+1):
        #sum[i] += j

Thread_count = len(ranges)
threads = []
sums = [0] * Thread_count

for i in range(Thread_count):

    start, end = ranges[i]

    t = threading.Thread(target=range_sum, args=(sums, i, start, end))
    t.start()
    
    threads.append(t)
    
for t in threads:
    t.join()

print(sums)
print(sum(sums))
