import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# PP Scheduling Algorithm
class Process:
    def __init__(self, name, arrival_time, burst_time, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority

class PP:
    def __init__(self):
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def schedule(self):
        schedule_log = []
        current_time = 0
        processes_copy = self.processes.copy()
        ready_queue = []
        while processes_copy or ready_queue:
            # Add arrived processes to ready queue
            for process in processes_copy[:]:
                if process.arrival_time <= current_time:
                    ready_queue.append(process)
                    processes_copy.remove(process)
            # Sort ready queue by priority
            ready_queue.sort(key=lambda x: x.priority, reverse=True)
            if ready_queue:
                process = ready_queue[0]
                # Execute process for 1 unit
                process.remaining_time -= 1
                schedule_log.append((process.name, current_time))
                # Check if process is completed
                if process.remaining_time == 0:
                    ready_queue.remove(process)
                current_time += 1
            else:
                current_time += 1
        return schedule_log

# Initialize Pygame
pygame.init()
display = (1280, 720)
screen = pygame.display.set_mode(display)
pygame.display.set_caption("Preemptive Priority Scheduling Krish Telang-205 Arya Torne-214 Varun Nagnure-296 Parth Sharma-324")

# Create PP scheduler
pp = PP()
pp.add_process(Process("P1", 0, 8, 3))
pp.add_process(Process("P2", 2, 4, 2))
pp.add_process(Process("P3", 4, 9, 1))
pp.add_process(Process("P4", 6, 5, 4))

# Schedule processes
schedule_log = pp.schedule()

# Main loop
clock = pygame.time.Clock()
running = True
process_index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with white
    screen.fill(WHITE)

    # Draw title
    font = pygame.font.SysFont("Arial", 20)
    title = font.render("Preemptive Priority Scheduling", True, BLACK)
    screen.blit(title, (200, 50))

    # Draw process names, arrival times, burst times, and priorities
    process_info = font.render("Processes:", True, BLACK)
    screen.blit(process_info, (100, 100))
    process_names = ["P1", "P2", "P3", "P4"]
    arrival_times = [0, 2, 4, 6]
    burst_times = [8, 4, 9, 5]
    priorities = [3, 2, 1, 4]
    for i in range(4):
        process_text = font.render(f"{process_names[i]}: AT={arrival_times[i]}, BT={burst_times[i]}, Priority={priorities[i]}", True, BLACK)
        screen.blit(process_text, (100, 150 + i*50))

    # Draw Gantt chart
    rect_height = 30
    rect_width = 80
    gantt_chart_x = 100
    gantt_chart_y = 400
    processes_per_row = 14
    for i in range(process_index+1):
        column = i % processes_per_row
        row_index = i // processes_per_row
        start_time = schedule_log[i][1]
        end_time = start_time + 1
        pygame.draw.rect(screen, GRAY, (gantt_chart_x, gantt_chart_y + row_index*120, processes_per_row*rect_width, rect_height), 1)
        pygame.draw.rect(screen, BLUE, (gantt_chart_x + column*rect_width, gantt_chart_y + row_index*120, rect_width-5, rect_height))
        pygame.draw.rect(screen, BLACK, (gantt_chart_x + column*rect_width, gantt_chart_y + row_index*120, rect_width-5, rect_height), 1)
        process_text = font.render(f"{schedule_log[i][0]}: {start_time}-{end_time}", True, BLACK)
        screen.blit(process_text, (gantt_chart_x + column*rect_width + 10, gantt_chart_y + row_index*120 + rect_height + 20))

    # Update display
    pygame.display.flip()
    clock.tick(1)

    # Increment process index
    if process_index < len(schedule_log) - 1:
        process_index += 1
    else:
        pygame.time.wait(2000)  # Wait for 2 seconds before quitting
        running = False

