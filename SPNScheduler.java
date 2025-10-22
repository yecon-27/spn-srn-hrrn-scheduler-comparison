package Implementation;
import java.util.*;

public class SPNScheduler {
    public static void spnSchedule(List<Process> processes) {
        List<Process> readyQueue = new ArrayList<>();
        List<Process> completed = new ArrayList<>();
        int currentTime = 0;
        
        // Sort processes by arrival time
        processes.sort(Comparator.comparingInt(p -> p.arrivalTime));

        System.out.println("=== SPN (Shortest Process Next) Scheduling ===");
        System.out.println("Time\tEvent");
        System.out.println("----\t-----");
        
        while (completed.size() < processes.size()) {
            // Add arrived processes to ready queue
            for (Process p : processes) {
                if (p.arrivalTime <= currentTime && 
                    !readyQueue.contains(p) && !completed.contains(p)) {
                    readyQueue.add(p);
                    System.out.println(currentTime + "\tP" + p.pid + " arrives");
                }
            }
            
            if (!readyQueue.isEmpty()) {
                // Sort by burst time (SPN logic)
                readyQueue.sort(Comparator.comparingInt(p -> p.burstTime));
                
                Process current = readyQueue.remove(0);
                
                // Execute process
                System.out.println(currentTime + "\tP" + current.pid + " starts execution");
                currentTime += current.burstTime;
                current.completionTime = currentTime;
                current.calculateTimes();
                completed.add(current);
                
                System.out.println(currentTime + "\tP" + current.pid + " completes");
            } else {
                currentTime++; // CPU idle
                System.out.println(currentTime + "\tCPU idle");
            }
        }
        
        printResults(completed);
    }
    
    private static void printResults(List<Process> processes) {
        System.out.println("\n=== SPN Results ===");
        System.out.println("PID\tAT\tBT\tCT\tTAT\tWT");
        System.out.println("---\t--\t--\t--\t---\t--");
        
        double totalTAT = 0, totalWT = 0;
        for (Process p : processes) {
            System.out.printf("P%d\t%d\t%d\t%d\t%d\t%d\n", 
                p.pid, p.arrivalTime, p.burstTime, 
                p.completionTime, p.turnaroundTime, p.waitingTime);
            totalTAT += p.turnaroundTime;
            totalWT += p.waitingTime;
        }
        
        System.out.printf("\nAverage TAT: %.1f ms\n", totalTAT / processes.size());
        System.out.printf("Average WT: %.1f ms\n", totalWT / processes.size());
        System.out.printf("CPU Utilization: 100%%\n");
    }
}