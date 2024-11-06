import pygame
import sys


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


class Process:
    def __init__(self, name, burst_time):
        self.name = name
        self.burst_time = burst_time

class RoundRobin:
    def __init__(self, quantum):
        self.quantum = quantum
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def schedule(self):
        time = 0
        schedule_log = []
        while True:
            finished = True
            for process in self.processes:
                if process.burst_time > 0:
                    finished = False
                    if process.burst_time <= self.quantum:
                        time += process.burst_time
                        process.burst_time = 0
                        schedule_log.append((process.name, time))
                    else:
                        process.burst_time -= self.quantum
                        time += self.quantum
                        schedule_log.append((process.name, time))
            if finished:
                break
        return schedule_log


pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display)
pygame.display.set_caption("Round Robin Scheduling Krish Telang-205 Arya Torne-214 Varun Nagnure-296 Parth Sharma-324 \n")


rr = RoundRobin(quantum=2)

rr.add_process(Process("P1", 8))
rr.add_process(Process("P2", 4))
rr.add_process(Process("P3", 9))
rr.add_process(Process("P4", 5))

schedule_log = rr.schedule()

clock = pygame.time.Clock()
running = True
process_values = [8, 4, 9, 5]
gantt_chart_x = 100
gantt_chart_log = []
process_names = ["P1", "P2", "P3", "P4"]
current_process = 0
time = 0
gantt_chart_y = 400
row_length = 15
decrement_counter = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill(WHITE)

    
    font = pygame.font.SysFont("Arial", 20)
    title = font.render("Round Robin Scheduling", True, BLACK)
    screen.blit(title, (300, 50))

    
    process_info = font.render("Processes:", True, BLACK)
    screen.blit(process_info, (100, 100))
    for i, process in enumerate(rr.processes):
        process_text = font.render(f"{process_names[i]}: {process_values[i]}", True, BLACK)
        screen.blit(process_text, (100, 150 + i*50))
        if process_values[current_process] > 0:
            decrement_counter += 1
            if decrement_counter == rr.quantum:
                process_values[current_process] = max(0, process_values[current_process] - rr.quantum)
                gantt_chart_log.append((process_names[current_process], process_values[current_process]))
                time += rr.quantum
                decrement_counter = 0
                current_process = (current_process + 1) % len(rr.processes)

    
    rect_height = 30  
    rect_width = 60  
    row_length = 10  
    gantt_chart_x = 100
    gantt_chart_y = 400
    row = 0
    while len(gantt_chart_log) > row_length * (row + 1):
        row += 1
    for i, (process_name, burst_time) in enumerate(gantt_chart_log):
        column = i % row_length
        row_index = i // row_length
        pygame.draw.rect(screen, GRAY, (gantt_chart_x, gantt_chart_y + row_index*120, row_length*rect_width, rect_height), 1)  
        pygame.draw.rect(screen, BLUE, (gantt_chart_x + column*rect_width, gantt_chart_y + row_index*120, rect_width-5, rect_height))
        pygame.draw.rect(screen, BLACK, (gantt_chart_x + column*rect_width, gantt_chart_y + row_index*120, rect_width-5, rect_height), 1)
        process_text = font.render(f"{process_name}: {burst_time}", True, BLACK)
        screen.blit(process_text, (gantt_chart_x + column*rect_width + 10, gantt_chart_y + row_index*120 + rect_height + 20))

    
    quantum_text = font.render(f"Quantum Time: {rr.quantum}", True, BLACK)
    screen.blit(quantum_text, (500, 100))

    
    pygame.display.flip()
    clock.tick(1)

    
    if all(value <= 0 for value in process_values):
        running = False

    
    if process_values[current_process] <= 0:
        current_process = (current_process + 1) % len(rr.processes)
        while process_values[current_process] <= 0:
            current_process = (current_process + 1) % len(rr.processes)
           