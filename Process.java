package Implementation;
class Process {
    int pid;
    int arrivalTime;
    int burstTime;
    int remainingTime;
    int completionTime;
    int turnaroundTime;
    int waitingTime;
    
    public Process(int pid, int arrivalTime, int burstTime) {
        this.pid = pid;
        this.arrivalTime = arrivalTime;
        this.burstTime = burstTime;
        this.remainingTime = burstTime;
    }
    
    public void calculateTimes() {
        this.turnaroundTime = this.completionTime - this.arrivalTime;
        this.waitingTime = this.turnaroundTime - this.burstTime;
    }
    
    @Override
    public String toString() {
        return String.format("P%d(AT:%d, BT:%d)", pid, arrivalTime, burstTime);
    }
}