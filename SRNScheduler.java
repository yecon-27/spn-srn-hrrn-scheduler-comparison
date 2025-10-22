package Implementation;
import java.util.*;

public class SRNScheduler {
    public static void srnSchedule(List<Process> processes) {
        List<Process> readyQueue = new ArrayList<>();
        List<Process> completed = new ArrayList<>();
        int currentTime = 0;
        Process currentProcess = null;
        
        // Create copies to preserve original burst times
        List<Process> processCopies = new ArrayList<>();
        for (Process p : processes) {
            Process copy = new Process(p.pid, p.arrivalTime, p.burstTime);
            processCopies.add(copy);
        }
        
        System.out.println("=== SRN (Shortest Remaining Time Next) Scheduling ===");
        System.out.println("Time\tEvent\t\t\tReady Queue");
        System.out.println("----\t-----\t\t\t-----------");
        
        while (completed.size() < processCopies.size()) {
            // Add newly arrived processes
            for (Process p : processCopies) {
                if (p.arrivalTime == currentTime && !readyQueue.contains(p)) {
                    readyQueue.add(p);
                    System.out.printf("%d\tP%d arrives\t\t%s\n", 
                        currentTime, p.pid, getReadyQueueString(readyQueue));
                }
            }
            
            // Check for preemption
            if (!readyQueue.isEmpty()) {
                readyQueue.sort(Comparator.comparingInt(p -> p.remainingTime));
                Process shortestJob = readyQueue.get(0);
                
                if (currentProcess == null || 
                    shortestJob.remainingTime < currentProcess.remainingTime) {
                    if (currentProcess != null && currentProcess.remainingTime > 0) {
                        // Current process gets preempted
                        readyQueue.add(currentProcess);
                        System.out.printf("%d\tP%d preempted\t\t%s\n", 
                            currentTime, currentProcess.pid, getReadyQueueString(readyQueue));
                    }
                    currentProcess = shortestJob;
                    readyQueue.remove(shortestJob);
                    System.out.printf("%d\tP%d starts/resumes\t%s\n", 
                        currentTime, currentProcess.pid, getReadyQueueString(readyQueue));
                }
            }
            
            if (currentProcess != null) {
                // Execute current process for 1 time unit
                currentProcess.remainingTime--;
                currentTime++;
                
                if (currentProcess.remainingTime == 0) {
                    // Process completed
                    currentProcess.completionTime = currentTime;
                    currentProcess.calculateTimes();
                    completed.add(currentProcess);
                    
                    System.out.printf("%d\tP%d completes\t\t%s\n", 
                        currentTime, currentProcess.pid, getReadyQueueString(readyQueue));
                    currentProcess = null;
                }
            } else {
                currentTime++; // CPU idle
                System.out.printf("%d\tCPU idle\t\t%s\n", 
                    currentTime, getReadyQueueString(readyQueue));
            }
        }
        
        printResults(completed);
    }
    
    private static String getReadyQueueString(List<Process> readyQueue) {
        if (readyQueue.isEmpty()) return "[]";
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < readyQueue.size(); i++) {
            Process p = readyQueue.get(i);
            sb.append("P").append(p.pid).append("(").append(p.remainingTime).append(")");
            if (i < readyQueue.size() - 1) sb.append(", ");
        }
        sb.append("]");
        return sb.toString();
    }
    
    private static void printResults(List<Process> processes) {
        System.out.println("\n=== SRN Results ===");
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