"""
CPU Scheduling Algorithms Implementation
Implements SPN, SRN (SRTF), and HRRN scheduling algorithms
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import heapq

@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    
@dataclass
class Result:
    pid: str
    arrival: int
    burst: int
    completion: int
    turnaround: int
    waiting: int
    
def spn_schedule(processes: List[Dict]) -> Dict:
    """
    Shortest Process Next (SPN) - Non-preemptive
    """
    procs = sorted([Process(**p) for p in processes], key=lambda x: (x.arrival, x.pid))
    n = len(procs)
    
    results = []
    gantt = []
    time = 0
    completed = []
    ready_queue = []
    
    while len(completed) < n:
        # Add all processes that have arrived to ready queue
        for p in procs:
            if p.arrival <= time and p not in completed and p not in ready_queue:
                ready_queue.append(p)
        
        if not ready_queue:
            # No process ready, jump to next arrival
            time = min(p.arrival for p in procs if p not in completed)
            continue
        
        # Select process with shortest burst time
        ready_queue.sort(key=lambda x: (x.burst, x.pid))
        current = ready_queue.pop(0)
        
        # Execute process to completion
        start_time = time
        time += current.burst
        gantt.append((current.pid, start_time, time))
        
        completion = time
        turnaround = completion - current.arrival
        waiting = turnaround - current.burst
        
        results.append(Result(
            pid=current.pid,
            arrival=current.arrival,
            burst=current.burst,
            completion=completion,
            turnaround=turnaround,
            waiting=waiting
        ))
        completed.append(current)
    
    # Calculate averages
    avg_tat = sum(r.turnaround for r in results) / n
    avg_wt = sum(r.waiting for r in results) / n
    
    # Calculate CPU utilization
    makespan = max(r.completion for r in results) - min(p.arrival for p in procs)
    total_burst = sum(p.burst for p in procs)
    cpu_util = total_burst / makespan if makespan > 0 else 0
    
    return {
        'results': sorted(results, key=lambda x: x.pid),
        'gantt': gantt,
        'avg_tat': avg_tat,
        'avg_wt': avg_wt,
        'cpu_util': cpu_util
    }

def srn_schedule(processes: List[Dict]) -> Dict:
    """
    Shortest Remaining Time Next (SRN/SRTF) - Preemptive
    """
    procs = sorted([Process(**p) for p in processes], key=lambda x: (x.arrival, x.pid))
    n = len(procs)
    
    remaining = {p.pid: p.burst for p in procs}
    completion = {p.pid: 0 for p in procs}
    first_start = {p.pid: None for p in procs}
    
    time = 0
    gantt = []
    idx = 0
    heap = []
    
    # Add first processes
    while idx < n and procs[idx].arrival <= time:
        p = procs[idx]
        heapq.heappush(heap, (remaining[p.pid], p.arrival, p.pid, p.burst))
        idx += 1
    
    if not heap:
        time = procs[0].arrival
        p = procs[0]
        heapq.heappush(heap, (remaining[p.pid], p.arrival, p.pid, p.burst))
        idx = 1
    
    while heap:
        rem, arr, pid, burst = heapq.heappop(heap)
        
        if first_start[pid] is None:
            first_start[pid] = time
        
        # Check next arrival
        next_arrival = procs[idx].arrival if idx < n else float('inf')
        
        if time + rem <= next_arrival:
            # Process completes before next arrival
            gantt.append((pid, time, time + rem))
            time += rem
            completion[pid] = time
            remaining[pid] = 0
            
            # Add newly arrived processes
            while idx < n and procs[idx].arrival <= time:
                p = procs[idx]
                heapq.heappush(heap, (remaining[p.pid], p.arrival, p.pid, p.burst))
                idx += 1
        else:
            # Preemption occurs
            run_time = next_arrival - time
            if run_time > 0:
                gantt.append((pid, time, next_arrival))
                remaining[pid] = rem - run_time
                time = next_arrival
            
            # Add newly arrived process
            p = procs[idx]
            heapq.heappush(heap, (remaining[p.pid], p.arrival, p.pid, p.burst))
            idx += 1
            
            # Re-add current process if not finished
            if remaining[pid] > 0:
                heapq.heappush(heap, (remaining[pid], arr, pid, burst))
    
    # Calculate results
    results = []
    for p in procs:
        ct = completion[p.pid]
        tat = ct - p.arrival
        wt = tat - p.burst
        results.append(Result(
            pid=p.pid,
            arrival=p.arrival,
            burst=p.burst,
            completion=ct,
            turnaround=tat,
            waiting=wt
        ))
    
    avg_tat = sum(r.turnaround for r in results) / n
    avg_wt = sum(r.waiting for r in results) / n
    
    makespan = max(completion.values()) - min(p.arrival for p in procs)
    total_burst = sum(p.burst for p in procs)
    cpu_util = total_burst / makespan if makespan > 0 else 0
    
    return {
        'results': sorted(results, key=lambda x: x.pid),
        'gantt': gantt,
        'avg_tat': avg_tat,
        'avg_wt': avg_wt,
        'cpu_util': cpu_util
    }

def hrrn_schedule(processes: List[Dict]) -> Dict:
    """
    Highest Response Ratio Next (HRRN) - Non-preemptive
    """
    procs = sorted([Process(**p) for p in processes], key=lambda x: (x.arrival, x.pid))
    n = len(procs)
    
    results = []
    gantt = []
    time = 0
    completed = []
    
    while len(completed) < n:
        # Get all arrived processes
        ready = [p for p in procs if p.arrival <= time and p not in completed]
        
        if not ready:
            # Jump to next arrival
            time = min(p.arrival for p in procs if p not in completed)
            ready = [p for p in procs if p.arrival <= time and p not in completed]
        
        # Calculate response ratio for each ready process
        response_ratios = []
        for p in ready:
            waiting_time = time - p.arrival
            response_ratio = (waiting_time + p.burst) / p.burst
            response_ratios.append((response_ratio, p.pid, p))
        
        # Select process with highest response ratio (break ties by PID)
        response_ratios.sort(key=lambda x: (-x[0], x[1]))
        current = response_ratios[0][2]
        
        # Execute process
        start_time = time
        time += current.burst
        gantt.append((current.pid, start_time, time))
        
        completion = time
        turnaround = completion - current.arrival
        waiting = turnaround - current.burst
        
        results.append(Result(
            pid=current.pid,
            arrival=current.arrival,
            burst=current.burst,
            completion=completion,
            turnaround=turnaround,
            waiting=waiting
        ))
        completed.append(current)
    
    avg_tat = sum(r.turnaround for r in results) / n
    avg_wt = sum(r.waiting for r in results) / n
    
    makespan = max(r.completion for r in results) - min(p.arrival for p in procs)
    total_burst = sum(p.burst for p in procs)
    cpu_util = total_burst / makespan if makespan > 0 else 0
    
    return {
        'results': sorted(results, key=lambda x: x.pid),
        'gantt': gantt,
        'avg_tat': avg_tat,
        'avg_wt': avg_wt,
        'cpu_util': cpu_util
    }

# Test with given data
if __name__ == "__main__":
    processes = [
        {"pid": "P1", "arrival": 0, "burst": 6},
        {"pid": "P2", "arrival": 2, "burst": 8},
        {"pid": "P3", "arrival": 4, "burst": 7},
        {"pid": "P4", "arrival": 5, "burst": 3},
    ]
    
    print("=== SPN Scheduling ===")
    spn_result = spn_schedule(processes)
    print("Gantt Chart:", spn_result['gantt'])
    for r in spn_result['results']:
        print(f"{r.pid}: CT={r.completion}, TAT={r.turnaround}, WT={r.waiting}")
    print(f"Avg TAT: {spn_result['avg_tat']:.2f}, Avg WT: {spn_result['avg_wt']:.2f}")
    print(f"CPU Utilization: {spn_result['cpu_util']*100:.2f}%\n")
    
    print("=== SRN/SRTF Scheduling ===")
    srn_result = srn_schedule(processes)
    print("Gantt Chart:", srn_result['gantt'])
    for r in srn_result['results']:
        print(f"{r.pid}: CT={r.completion}, TAT={r.turnaround}, WT={r.waiting}")
    print(f"Avg TAT: {srn_result['avg_tat']:.2f}, Avg WT: {srn_result['avg_wt']:.2f}")
    print(f"CPU Utilization: {srn_result['cpu_util']*100:.2f}%\n")
    
    print("=== HRRN Scheduling ===")
    hrrn_result = hrrn_schedule(processes)
    print("Gantt Chart:", hrrn_result['gantt'])
    for r in hrrn_result['results']:
        print(f"{r.pid}: CT={r.completion}, TAT={r.turnaround}, WT={r.waiting}")
    print(f"Avg TAT: {hrrn_result['avg_tat']:.2f}, Avg WT: {hrrn_result['avg_wt']:.2f}")
    print(f"CPU Utilization: {hrrn_result['cpu_util']*100:.2f}%")
