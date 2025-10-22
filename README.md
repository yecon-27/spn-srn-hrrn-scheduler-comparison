# CPU Scheduling Algorithms - Assignment Deliverables

## Overview
We analyze three CPU scheduling algorithms: SPN (Shortest Process Next), SRN/SRTF (Shortest Remaining Time First), and HRRN (Highest Response Ratio Next).

## Language
Both Java and Python

### Python Implementation
- **scheduling_algorithms.py** - Core implementation of all three algorithms
  - `spn_schedule()` - Shortest Process Next
  - `srn_schedule()` - Shortest Remaining Time Next (SRTF)
  - `hrrn_schedule()` - Highest Response Ratio Next
  - Includes test cases and metric calculations

- **generate_gantt_charts.py** - Visualization script
  - Creates individual Gantt charts for each algorithm
  - Generates combined comparison chart
  - Uses matplotlib for high-quality graphics

### Gantt Charts (PNG images)
- **spn_gantt.png** - SPN scheduling visualization
- **srn_gantt.png** - SRN/SRTF scheduling visualization (showing preemptions)
- **hrrn_gantt.png** - HRRN scheduling visualization
- **combined_gantt.png** - Side-by-side comparison of all three algorithms

## Process Data Used
| Process | Arrival Time (ms) | Burst Time (ms) |
|---------|-------------------|-----------------|
| P1      | 0                 | 6               |
| P2      | 2                 | 8               |
| P3      | 4                 | 7               |
| P4      | 5                 | 3               |

## Results Summary

### SPN (Shortest Process Next)
- Execution Order: P1 → P4 → P3 → P2
- Average TAT: 11.00 ms
- Average WT: 5.00 ms
- CPU Utilization: 100%

### SRN/SRTF (Shortest Remaining Time First)
- Execution Order: P1 → P4 → P3 → P2 (with preemption points)
- Average TAT: 11.00 ms
- Average WT: 5.00 ms
- CPU Utilization: 100%

### HRRN (Highest Response Ratio Next)
- Execution Order: P1 → P2 → P4 → P3
- Average TAT: 12.50 ms
- Average WT: 6.50 ms
- CPU Utilization: 100%

## How to Run the Code

### Requirements
```bash
pip install matplotlib numpy
```

### Run Scheduling Algorithms
```bash
python3 scheduling_algorithms.py
```

### Generate Gantt Charts
```bash
python3 generate_gantt_charts.py
```

## Key Findings
1. **Best for Average TAT/WT**: SPN and SRN/SRTF (tied at 11.00 ms TAT, 5.00 ms WT)
2. **Best for Fairness**: HRRN (prevents starvation of long processes)
3. **Best for Batch Systems**: SRN/SRTF (preemptive, optimal average TAT)
4. **Best for Interactive Systems**: HRRN (balances efficiency and fairness)

