import pygame
import sys
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 500
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Simulación de Colisiones Elásticas')

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Frecuencia de actualización
clock = pygame.time.Clock()
FPS = 60



class Ball:
    def __init__(self, x, y, radius, color, velocity_x, mass):
        self.x = x
        self.y = y
        self.radius = mass * 5
        self.color = color
        self.velocity_x = velocity_x
        self.mass = mass

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self, window_width):
        # Actualiza la posición x con la velocidad
        self.x += self.velocity_x

        # Comprueba si la pelota está fuera de los límites de la pantalla y ajusta la velocidad
        if self.x - self.radius <= 0 or self.x + self.radius >= window_width:
            self.velocity_x *= -1  # Invierte la dirección en el eje x

    def kinetic_energy(self):
        # E_k = 1/2 * m * v^2
        return 0.5 * self.mass * (self.velocity_x ** 2)
    



def display_info(window, balls):
    total_energy = sum(ball.kinetic_energy() for ball in balls)
    y_offset = 0
    for i, ball in enumerate(balls, start=1):
        text = f"Ball {i} kinetic energy {ball.kinetic_energy():.2f} J velocity {ball.velocity_x:.2f} m/s mass {ball.mass:.1f} kg"
        label = pygame.font.SysFont(None, 24).render(text, 1, WHITE)
        window.blit(label, (10, y_offset))
        y_offset += 25
    
    total_energy_text = f"Total energy {total_energy:.2f} J"
    total_label = pygame.font.SysFont(None, 24).render(total_energy_text, 1, WHITE)
    window.blit(total_label, (10, y_offset))


def check_collision(ball1, ball2):
    dx = ball1.x - ball2.x
    distance = abs(dx)
    return distance < (ball1.radius + ball2.radius)

def handle_collisions(balls):
    num_balls = len(balls)
    for i in range(num_balls):
        for j in range(i + 1, num_balls):
            ball1, ball2 = balls[i], balls[j]
            if check_collision(ball1, ball2):
                # Calcular nuevas velocidades en el eje x después de la colisión
                v1_initial = ball1.velocity_x
                v2_initial = ball2.velocity_x

                # Conservación del momento (p = m * v)
                # m1 * v1_initial + m2 * v2_initial = m1 * v1_final + m2 * v2_final
                # Conservación de la energía cinética (Ec = 1/2 * m * v^2)
                # 1/2 * m1 * v1_initial^2 + 1/2 * m2 * v2_initial^2 = 1/2 * m1 * v1_final^2 + 1/2 * m2 * v2_final^2

                # Resolver para v1_final y v2_final
                v1_final = (v1_initial * (ball1.mass - ball2.mass) + 2 * ball2.mass * v2_initial) / (ball1.mass + ball2.mass)
                v2_final = (v2_initial * (ball2.mass - ball1.mass) + 2 * ball1.mass * v1_initial) / (ball1.mass + ball2.mass)

                ball1.velocity_x = v1_final
                ball2.velocity_x = v2_final



def main():
    ball1 = Ball(100, 200, 5, (255, 255, 0), 6, 3.0)  # masa de 1.0 kg
    ball2 = Ball(300, 200, 10, (0, 255, 0), -2, 1.0)    # masa de 1.5 kg
    ball3 = Ball(500, 200, 20, (255, 0, 0), 4, 6.0)   # masa de 2.0 kg


    
    balls = [ball1, ball2, ball3]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        windowSurface.fill(BLACK)

        for ball in balls:
            ball.move(WINDOW_WIDTH)
            ball.draw(windowSurface)

        handle_collisions(balls)

        display_info(windowSurface, balls)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()


