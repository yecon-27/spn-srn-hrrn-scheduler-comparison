package Implementation;
import java.util.*;

public class CPUSchedulingDemo {
    public static void main(String[] args) {
        // Create the processes with the given data
        List<Process> processes = Arrays.asList(
            new Process(1, 0, 8),
            new Process(2, 1, 4),
            new Process(3, 2, 9),
            new Process(4, 3, 5),
            new Process(5, 4, 2)
        );
        
        System.out.println("=== CPU Scheduling Algorithms Comparison ===\n");
        
        // Test SPN Scheduler
        System.out.println("1. SPN (Shortest Process Next) Scheduling:");
        System.out.println("=" .repeat(50));
        List<Process> spnProcesses = new ArrayList<>();
        for (Process p : processes) {
            spnProcesses.add(new Process(p.pid, p.arrivalTime, p.burstTime));
        }
        SPNScheduler.spnSchedule(spnProcesses);
        
        System.out.println("\n" + "=" .repeat(70) + "\n");
        
        // Test SRN Scheduler
        System.out.println("2. SRN (Shortest Remaining Time Next) Scheduling:");
        System.out.println("=" .repeat(50));
        List<Process> srnProcesses = new ArrayList<>();
        for (Process p : processes) {
            srnProcesses.add(new Process(p.pid, p.arrivalTime, p.burstTime));
        }
        SRNScheduler.srnSchedule(srnProcesses);
        
        System.out.println("\n" + "=" .repeat(70) + "\n");
        
        // Test HRRN Scheduler
        System.out.println("3. HRRN (Highest Response Ratio Next) Scheduling:");
        System.out.println("=" .repeat(50));
        List<Process> hrrnProcesses = new ArrayList<>();
        for (Process p : processes) {
            hrrnProcesses.add(new Process(p.pid, p.arrivalTime, p.burstTime));
        }
        HRRNScheduler.hrrnSchedule(hrrnProcesses);
        
        // Summary comparison
        System.out.println("\n" + "=" .repeat(70));
        System.out.println("SUMMARY COMPARISON");
        System.out.println("=" .repeat(70));
        
        // Calculate and display summary for each algorithm
        calculateSummary("SPN", processes);
        calculateSummary("SRN", processes);
        calculateSummary("HRRN", processes);
    }
    
    private static void calculateSummary(String algorithm, List<Process> originalProcesses) {
        List<Process> processes = new ArrayList<>();
        for (Process p : originalProcesses) {
            processes.add(new Process(p.pid, p.arrivalTime, p.burstTime));
        }
        
        double avgTAT = 0, avgWT = 0;
        
        switch (algorithm) {
            case "SPN":
                SPNScheduler.spnSchedule(processes);
                break;
            case "SRN":
                SRNScheduler.srnSchedule(processes);
                break;
            case "HRRN":
                HRRNScheduler.hrrnSchedule(processes);
                break;
        }
        
        for (Process p : processes) {
            avgTAT += p.turnaroundTime;
            avgWT += p.waitingTime;
        }
        
        avgTAT /= processes.size();
        avgWT /= processes.size();
        
        System.out.printf("%-6s | Avg TAT: %6.2f | Avg WT: %6.2f%n", 
                         algorithm, avgTAT, avgWT);
    }
}