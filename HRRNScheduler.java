package Implementation;
import java.util.*;

public class HRRNScheduler {
    public static void hrrnSchedule(List<Process> processes) {
        List<Process> readyQueue = new ArrayList<>();
        List<Process> completed = new ArrayList<>();
        int currentTime = 0;
        
        processes.sort(Comparator.comparingInt(p -> p.arrivalTime));
        
        System.out.println("=== HRRN (Highest Response Ratio Next) Scheduling ===");
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
                // Calculate response ratios and select highest
                Process selectedProcess = null;
                double highestRatio = -1;
                
                System.out.println("\n--- Response Ratio Calculations at time " + currentTime + " ---");
                for (Process p : readyQueue) {
                    int waitingTime = currentTime - p.arrivalTime;
                    double responseRatio = (double)(waitingTime + p.burstTime) / p.burstTime;
                    
                    System.out.printf("P%d: RR = (%d + %d) / %d = %.2f\n",
                        p.pid, waitingTime, p.burstTime, p.burstTime, responseRatio);
                    
                    if (responseRatio > highestRatio) {
                        highestRatio = responseRatio;
                        selectedProcess = p;
                    }
                }
                
                // Execute selected process
                readyQueue.remove(selectedProcess);
                System.out.printf("\nSelected: P%d (RR = %.2f)\n", 
                    selectedProcess.pid, highestRatio);
                System.out.println(currentTime + "\tP" + selectedProcess.pid + " starts execution");
                
                currentTime += selectedProcess.burstTime;
                selectedProcess.completionTime = currentTime;
                selectedProcess.calculateTimes();
                completed.add(selectedProcess);
                
                System.out.println(currentTime + "\tP" + selectedProcess.pid + " completes\n");
            } else {
                currentTime++; // CPU idle
                System.out.println(currentTime + "\tCPU idle");
            }
        }
        
        printResults(completed);
    }
    
    private static void printResults(List<Process> processes) {
        System.out.println("=== HRRN Results ===");
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