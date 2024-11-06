import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# SJF Scheduling Algorithm
class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time

class SJF:
    def __init__(self):
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def schedule(self):
        schedule_log = []
        current_time = 0
        processes_copy = self.processes.copy()
        while processes_copy:
            # Sort processes by arrival time
            processes_copy.sort(key=lambda x: x.arrival_time)
            # Get the process with the earliest arrival time
            arrived_processes = [p for p in processes_copy if p.arrival_time <= current_time]
            arrived_processes.sort(key=lambda x: x.burst_time)
            process = arrived_processes.pop(0)
            # Remove process from processes_copy
            processes_copy.remove(process)
            # Add process to schedule log
            schedule_log.append((process.name, current_time))
            # Update current time
            current_time += process.burst_time
        return schedule_log

# Initialize Pygame
pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display)
pygame.display.set_caption("SJF Scheduling")

# Create SJF scheduler
sjf = SJF()
sjf.add_process(Process("P1", 0, 8))
sjf.add_process(Process("P2", 2, 4))
sjf.add_process(Process("P3", 4, 9))
sjf.add_process(Process("P4", 6, 5))

# Schedule processes
schedule_log = sjf.schedule()

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
    title = font.render("Shortest Job First Scheduling", True, BLACK)
    screen.blit(title, (300, 50))

    # Draw process names and burst times
    process_info = font.render("Processes:", True, BLACK)
    screen.blit(process_info, (100, 100))
    process_names = ["P1", "P2", "P3", "P4"]
    arrival_times = [0, 2, 4, 6]
    burst_times = [8, 4, 9, 5]
    for i in range(4):
        process_text = font.render(f"{process_names[i]}: AT={arrival_times[i]}, BT={burst_times[i]}", True, BLACK)
        screen.blit(process_text, (100, 150 + i*50))

    # Draw Gantt chart
    rect_height = 30
    rect_width = 80
    gantt_chart_x = 100
    gantt_chart_y = 400
    for i in range(process_index+1):
        column = i % 4
        row_index = i // 4
        start_time = schedule_log[i][1]
        end_time = start_time + [p.burst_time for p in sjf.processes if p.name == schedule_log[i][0]][0]
        pygame.draw.rect(screen, GRAY, (gantt_chart_x, gantt_chart_y + row_index*120, 4*rect_width, rect_height), 1)
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

# Quit Pygame
pygame.quit()
sys.exit()