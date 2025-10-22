"""
Generate Gantt Charts for CPU Scheduling Algorithms
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scheduling_algorithms import spn_schedule, srn_schedule, hrrn_schedule

def create_gantt_chart(gantt_data, title, filename):
    """
    Create a Gantt chart from scheduling data
    """
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # Extract unique process IDs and assign colors
    processes = sorted(list(set(pid for pid, _, _ in gantt_data)))
    colors = ['#5DADE2', '#48C9B0', '#F4D03F', '#E74C3C', '#AF7AC5', '#EC7063']
    color_map = {pid: colors[i % len(colors)] for i, pid in enumerate(processes)}
    
    # Find y-position for each process
    y_positions = {pid: 10 + i * 15 for i, pid in enumerate(processes)}
    
    # Draw bars
    for pid, start, end in gantt_data:
        duration = end - start
        ax.broken_barh([(start, duration)], 
                       (y_positions[pid], 10), 
                       facecolors=color_map[pid],
                       edgecolor='black',
                       linewidth=0.5)
        # Add time labels
        mid_point = start + duration / 2
        ax.text(mid_point, y_positions[pid] + 5, 
                f"{start}–{end}", 
                ha='center', va='center', 
                fontsize=9, fontweight='bold')
    
    # Configure axes
    ax.set_xlabel('Time (ms)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Processes', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Set y-axis
    ax.set_yticks([y_positions[pid] + 5 for pid in processes])
    ax.set_yticklabels(processes)
    
    # Set x-axis
    max_time = max(end for _, _, end in gantt_data)
    ax.set_xlim(0, max_time + 1)
    ax.set_ylim(0, max(y_positions.values()) + 20)
    
    # Add grid
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Saved {filename}")
    plt.close()

def create_combined_gantt(spn_gantt, srn_gantt, hrrn_gantt, filename):
    """
    Create a combined figure with all three Gantt charts
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 8))
    
    processes = ['P1', 'P2', 'P3', 'P4']
    colors = {'P1': '#5DADE2', 'P2': '#48C9B0', 'P3': '#F4D03F', 'P4': '#E74C3C'}
    
    gantt_data = [
        (spn_gantt, "SPN (Shortest Process Next)", axes[0]),
        (srn_gantt, "SRN/SRTF (Shortest Remaining Time First)", axes[1]),
        (hrrn_gantt, "HRRN (Highest Response Ratio Next)", axes[2])
    ]
    
    for gantt, title, ax in gantt_data:
        y_positions = {pid: 10 + i * 15 for i, pid in enumerate(processes)}
        
        for pid, start, end in gantt:
            duration = end - start
            ax.broken_barh([(start, duration)], 
                           (y_positions[pid], 10), 
                           facecolors=colors[pid],
                           edgecolor='black',
                           linewidth=0.5)
            mid_point = start + duration / 2
            ax.text(mid_point, y_positions[pid] + 5, 
                    f"{start}–{end}", 
                    ha='center', va='center', 
                    fontsize=8, fontweight='bold')
        
        ax.set_ylabel('Process', fontsize=10, fontweight='bold')
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_yticks([y_positions[pid] + 5 for pid in processes])
        ax.set_yticklabels(processes)
        ax.set_xlim(0, 25)
        ax.set_ylim(0, max(y_positions.values()) + 20)
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    
    axes[-1].set_xlabel('Time (ms)', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Saved {filename}")
    plt.close()

if __name__ == "__main__":
    processes = [
        {"pid": "P1", "arrival": 0, "burst": 6},
        {"pid": "P2", "arrival": 2, "burst": 8},
        {"pid": "P3", "arrival": 4, "burst": 7},
        {"pid": "P4", "arrival": 5, "burst": 3},
    ]
    
    # Run scheduling algorithms
    spn_result = spn_schedule(processes)
    srn_result = srn_schedule(processes)
    hrrn_result = hrrn_schedule(processes)
    
    # Create individual Gantt charts
    create_gantt_chart(spn_result['gantt'], 
                      "SPN (Shortest Process Next) Scheduling",
                      "spn_gantt.png")
    
    create_gantt_chart(srn_result['gantt'], 
                      "SRN/SRTF (Shortest Remaining Time First) Scheduling",
                      "srn_gantt.png")
    
    create_gantt_chart(hrrn_result['gantt'], 
                      "HRRN (Highest Response Ratio Next) Scheduling",
                      "hrrn_gantt.png")
    
    # Create combined chart
    create_combined_gantt(spn_result['gantt'], 
                         srn_result['gantt'], 
                         hrrn_result['gantt'],
                         "combined_gantt.png")
    
    print("\nAll Gantt charts generated successfully!")
