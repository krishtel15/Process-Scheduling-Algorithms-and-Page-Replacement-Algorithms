import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("Arial", 20)

class Process:
    def __init__(self, arrival_time, burst_time):
        self.arrival_time = arrival_time
        self.burst_time = burst_time

def draw_gantt_chart(processes):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Sort processes by arrival time
    processes.sort(key=lambda x: x.arrival_time)

    running_time = 0
    x = 50

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        for i, process in enumerate(processes):
            running_time += process.burst_time
            pygame.draw.rect(screen, BLACK, (x, 100, process.burst_time * 10, 50))
            pygame.draw.rect(screen, WHITE, (x, 90, process.burst_time * 10, 10))
            text = FONT.render(f"P{i+1} ({process.arrival_time}, {process.burst_time})", True, BLACK)
            screen.blit(text, (x, 80))
            text = FONT.render(str(running_time), True, BLACK)
            screen.blit(text, (x + process.burst_time * 10 - 20, 120))
            x += process.burst_time * 10 + 20

        pygame.display.flip()
        clock.tick(60)

def main():
    num_processes = int(input("Enter number of processes: "))

    processes = []
    for i in range(num_processes):
        arrival_time = int(input(f"Enter arrival time for process {i+1}: "))
        burst_time = int(input(f"Enter burst time for process {i+1}: "))
        processes.append(Process(arrival_time, burst_time))

    draw_gantt_chart(processes)

if __name__ == "__main__":
    main()