import pygame
import math
import random
from win32gui import SetWindowPos


class Visualisation:
    # Rozmiar okna
    WIDTH, HEIGHT = 1580, 820

    # Czas
    TIME_WIDTH = WIDTH
    TIME_HEIGHT = HEIGHT // 10
    month_iterator = 1
    year_iterator = 1
    
    # Budżet
    budget = 0

    # Legenda
    LEGEND_WIDTH = WIDTH // 9
    LEGEND_HEIGHT = HEIGHT - TIME_HEIGHT

    # Główne okno
    MAIN_WIDTH = (WIDTH // 10) * 9
    MAIN_HEIGHT = HEIGHT - TIME_HEIGHT



    # Czcionka
    FONT_SIZE = 24
    TIME_FONT_SIZE = 30

    # Okręgi
    circle_width = 600
    circle_height = 600
    CIRCLE_RADIUS = 10
    BUDGET_CIRCLE_RADIUS = 0

    # kropki (jednostki)
    UNIT_CIRCLE_RADIUS = 5

    # Kolor dla ramek, tekstu i symboli
    WHITE = (255, 255, 255)
    PINK = (208, 59, 203)
    BLUE = (46, 165, 216)
    GREY = (158, 155, 155)
    GREEN = (54, 192, 59)
    RED = (243, 16, 16)
    YOUNG_COLOR = (255, 127, 39)
    MIDDLE_COLOR = (128, 128, 64)
    OLD_COLOR = (128, 0, 64)

    # Kolory dla paska czasu
    BAR_HEIGHT = 20
    LOADING_PART = 0.1
    BLUE_BAR = (0, 0, 255)
    GREEN_BAR = (0, 255, 0)
    YELLOW_BAR = (255, 255, 0)
    RED_BAR = (255, 0, 0)

    # tablice punktów (jednostek)
    death_unit_list = []
    accident_unit_list = []
    people_unit_list = []

    # 3 liczniki, każdy dla osobnego wieku
    age_young_counter = 0
    age_middle_counter = 0
    age_old_counter = 0

    # ikona budżetu
    coin_icon = pygame.image.load('./coin_icon.png')

    @staticmethod
    def generate_point_in_circle_quarter(RADIUS, x_center, y_center, start_degree, end_degree):
        r = math.sqrt(random.random()) * RADIUS
        theta = random.uniform(start_degree, end_degree)

        x = r * math.cos(theta) + x_center
        y = r * math.sin(theta) + y_center

        return x, y

    @staticmethod
    def add_unit_to_section(section, gender):
        if gender == 1:
            color = Visualisation.BLUE
        else:
            color = Visualisation.PINK

        if section == "death":
            Visualisation.death_unit_list.append(
                (color,
                 Visualisation.generate_point_in_circle_quarter(Visualisation.circle_width // 2, Visualisation.WIDTH, 0,
                                                                -3 / 2 * math.pi, - math.pi)))
        elif section == "accident":
            Visualisation.accident_unit_list.append((color,
                                                     Visualisation.generate_point_in_circle_quarter(
                                                         Visualisation.circle_width // 2,
                                                         Visualisation.WIDTH,
                                                         Visualisation.MAIN_HEIGHT,
                                                         math.pi,
                                                         3 / 2 * math.pi)))
        elif section == "people":
            Visualisation.people_unit_list.append((color,
                                                   Visualisation.generate_point_in_circle_quarter(
                                                       Visualisation.circle_width // 2,
                                                       Visualisation.LEGEND_WIDTH,
                                                       0, 0, math.pi / 2)))

    @staticmethod
    def remove_unit_from_section(section, gender):
        if section == "people":
            if gender == 1:
                for item in Visualisation.people_unit_list:
                    if item[0] == Visualisation.BLUE:
                        Visualisation.people_unit_list.remove(item)
                        break
            else:
                for item in Visualisation.people_unit_list:
                    if item[0] == Visualisation.PINK:
                        Visualisation.people_unit_list.remove(item)
                        break

        else:
            if gender == 1:
                for item in Visualisation.age_young_unit_list:
                    if item[0] == Visualisation.BLUE:
                        Visualisation.age_young_unit_list.remove(item)
                        break
            else:
                for item in Visualisation.age_young_unit_list:
                    if item[0] == Visualisation.PINK:
                        Visualisation.age_young_unit_list.remove(item)
                        break

    @staticmethod
    def start_visualisation():
        pygame.init()
        win = pygame.display.set_mode((Visualisation.WIDTH, Visualisation.HEIGHT))

        # Automatyczne pojawianie się okna pygame na 1 planie
        SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 0, 0, 0, 1)

        # Inicjalizacja czcionki
        font = pygame.font.Font(None, Visualisation.FONT_SIZE)
        time_font = pygame.font.Font(None, Visualisation.TIME_FONT_SIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # Wypełnienie całego okna szarym kolorem
        win.fill(Visualisation.GREY)

        # # ----------------------------------LEGENDA--------------------------------------------#
        # Rysowanie ramki dla legendy
        pygame.draw.rect(win, Visualisation.WHITE, (0, 0, Visualisation.LEGEND_WIDTH, Visualisation.LEGEND_HEIGHT), 1)

        # Rysowanie tytułu legendy
        title_surface = font.render("LEGENDA", True, Visualisation.WHITE)
        win.blit(title_surface, (Visualisation.LEGEND_WIDTH // 2 - title_surface.get_width() // 2, 10))

        # Legenda - Kobiety
        pygame.draw.circle(win, Visualisation.PINK, (Visualisation.LEGEND_WIDTH // 6, 60),
                           Visualisation.CIRCLE_RADIUS)
        women_surface = font.render("Kobiety", True, Visualisation.WHITE)
        win.blit(women_surface, (
            Visualisation.LEGEND_WIDTH // 6 + Visualisation.CIRCLE_RADIUS + 7, 60 - Visualisation.FONT_SIZE // 3))

        # Legenda - Mężczyźni
        pygame.draw.circle(win, Visualisation.BLUE, (Visualisation.LEGEND_WIDTH // 6, 110),
                           Visualisation.CIRCLE_RADIUS)
        men_surface = font.render("Mężczyźni", True, Visualisation.WHITE)
        win.blit(men_surface, (
            Visualisation.LEGEND_WIDTH // 6 + Visualisation.CIRCLE_RADIUS + 7, 110 - Visualisation.FONT_SIZE // 3))

        # Legenda - Młodzi
        pygame.draw.rect(win, Visualisation.YOUNG_COLOR, pygame.Rect(Visualisation.LEGEND_WIDTH // 10, 540, 20, 20))
        young_surface = font.render("Osoby młode", True, Visualisation.WHITE)
        win.blit(young_surface, (
            Visualisation.LEGEND_WIDTH // 6 + Visualisation.CIRCLE_RADIUS + 7, 550 - Visualisation.FONT_SIZE // 3))

        # Legenda - W średnim wieku
        pygame.draw.rect(win, Visualisation.MIDDLE_COLOR, pygame.Rect(Visualisation.LEGEND_WIDTH // 10, 592, 20, 20))
        middle_surface_1 = font.render("Osoby w", True, Visualisation.WHITE)
        middle_surface_2 = font.render("średnim wieku", True, Visualisation.WHITE)
        win.blit(middle_surface_1, (
            Visualisation.LEGEND_WIDTH // 6 + Visualisation.CIRCLE_RADIUS + 7, 600 - Visualisation.FONT_SIZE // 3))
        win.blit(middle_surface_2, (
            Visualisation.LEGEND_WIDTH // 6 + Visualisation.CIRCLE_RADIUS + 7, 630 - Visualisation.FONT_SIZE // 3))

        # Legenda - Starzy
        pygame.draw.rect(win, Visualisation.OLD_COLOR, pygame.Rect(Visualisation.LEGEND_WIDTH // 10, 670, 20, 20))
        old_surface = font.render("Osoby starsze", True, Visualisation.WHITE)
        win.blit(old_surface, (
            Visualisation.LEGEND_WIDTH // 6 + Visualisation.CIRCLE_RADIUS + 7, 680 - Visualisation.FONT_SIZE // 3))

        # ---------------------------------GŁÓWNA RAMKA---------------------------------------#
        # Rysowanie ramki dla dużego prostokąta
        pygame.draw.rect(win, Visualisation.WHITE,
                         (Visualisation.LEGEND_WIDTH, 0, Visualisation.MAIN_WIDTH, Visualisation.MAIN_HEIGHT), 1)

        # Rysowanie krawędzi ćwiartek okręgu
        
        # Współrzędne krawędzi ćwiartki okręgu liczby ludzi
        circle_top_left_x = Visualisation.LEGEND_WIDTH - Visualisation.circle_width // 2
        circle_top_left_y = - Visualisation.circle_height // 2

        # Współrzędne krawędzi ćwiartki okręgu wieku ludzi
        circle_bottom_left_x = Visualisation.LEGEND_WIDTH - Visualisation.circle_width // 2
        circle_bottom_left_y = Visualisation.MAIN_HEIGHT - Visualisation.circle_height // 2

        # Współrzędne krawędzi ćwiartki okręgu śmierci ludzi
        circle_top_right_x = Visualisation.WIDTH - Visualisation.circle_width // 2
        circle_top_right_y = - Visualisation.circle_height // 2

        # Współrzędne krawędzi ćwiartki okręgu wypadków ludzi
        circle_bottom_right_x = Visualisation.WIDTH - Visualisation.circle_width // 2
        circle_bottom_right_y = Visualisation.MAIN_HEIGHT - Visualisation.circle_height // 2

        pygame.draw.arc(win, Visualisation.WHITE, [circle_top_left_x, circle_top_left_y, Visualisation.circle_width,
                                                   Visualisation.circle_height], math.radians(270), math.radians(360), 5)

        # -----------------------------------WYKRES KOŁOWY [MŁODZI, ŚREDNI, STARZY]---------------------------------------------#

        total_sum = Visualisation.age_young_counter + Visualisation.age_middle_counter + Visualisation.age_old_counter + 1
        old_angle = (Visualisation.age_old_counter / total_sum) * 90
        middle_angle = (Visualisation.age_middle_counter / total_sum) * 90
        # Wycinek kołowy - Starzy ludzie
        pygame.draw.arc(win, Visualisation.OLD_COLOR,
                        [circle_bottom_left_x, circle_bottom_left_y, Visualisation.circle_width,
                         Visualisation.circle_height], math.radians(0), math.radians(old_angle), 500)
        # Wycinek kołowy - ludzie w średnim wieku
        pygame.draw.arc(win, Visualisation.MIDDLE_COLOR,
                        [circle_bottom_left_x, circle_bottom_left_y, Visualisation.circle_width,
                         Visualisation.circle_height], math.radians(old_angle),
                        math.radians(old_angle) + math.radians(middle_angle), 500)
        # Wycinek kołowy - Młodzi ludzie
        pygame.draw.arc(win, Visualisation.YOUNG_COLOR,
                        [circle_bottom_left_x, circle_bottom_left_y, Visualisation.circle_width,
                         Visualisation.circle_height], math.radians(old_angle) + math.radians(middle_angle),
                        math.radians(90), 500)

        pygame.draw.arc(win, Visualisation.WHITE, [circle_top_right_x, circle_top_right_y, Visualisation.circle_width,
                        Visualisation.circle_height], math.radians(-180), math.radians(-90), 5)

        pygame.draw.arc(win, Visualisation.WHITE,
                        [circle_bottom_right_x, circle_bottom_right_y, Visualisation.circle_width,
                         Visualisation.circle_height], math.radians(90), math.radians(180), 5)

        #-------------------------------------------BUDŻET--------------------------------------------------#
        if 0 <= Visualisation.BUDGET_CIRCLE_RADIUS < 300:
            Visualisation.BUDGET_CIRCLE_RADIUS = Visualisation.budget * 300 / 22000000

        new_height = Visualisation.BUDGET_CIRCLE_RADIUS * 2
        new_width = Visualisation.BUDGET_CIRCLE_RADIUS * 2

        coin_pos_x = Visualisation.LEGEND_WIDTH + Visualisation.MAIN_WIDTH // 2 - new_width // 2
        coin_pos_y = Visualisation.MAIN_HEIGHT // 2 - new_height // 2

        resized_icon = pygame.transform.scale(Visualisation.coin_icon, (Visualisation.BUDGET_CIRCLE_RADIUS * 2, Visualisation.BUDGET_CIRCLE_RADIUS * 2))
        win.blit(resized_icon, (coin_pos_x, coin_pos_y))
        # --------------------------------------SEKCJE-----------------------------------------------------#
        # Śmierci
        death_surface = font.render("Śmierci", True, Visualisation.WHITE)
        win.blit(death_surface, (Visualisation.WIDTH - Visualisation.circle_width // 1.5, 10))
        for i in range(len(Visualisation.death_unit_list)):
            pygame.draw.circle(win, Visualisation.death_unit_list[i][0],
                               (Visualisation.death_unit_list[i][1][0], Visualisation.death_unit_list[i][1][1]),
                               Visualisation.UNIT_CIRCLE_RADIUS)

        # Wypadki
        accident_surface = font.render("Wypadki", True, Visualisation.WHITE)
        win.blit(accident_surface,
                 (Visualisation.WIDTH - Visualisation.circle_width // 1.5, Visualisation.MAIN_HEIGHT - 20))
        for i in range(len(Visualisation.accident_unit_list)):
            pygame.draw.circle(win, Visualisation.accident_unit_list[i][0],
                               (Visualisation.accident_unit_list[i][1][0], Visualisation.accident_unit_list[i][1][1]),
                               Visualisation.UNIT_CIRCLE_RADIUS)

        # Wiek
        age_surface = font.render("Wiek", True, Visualisation.WHITE)
        win.blit(age_surface,
                 (Visualisation.LEGEND_WIDTH + Visualisation.circle_width // 1.75, Visualisation.MAIN_HEIGHT - 20))

        # Liczba osób
        people_surface = font.render("Liczba osób", True, Visualisation.WHITE)
        win.blit(people_surface, (Visualisation.LEGEND_WIDTH + Visualisation.circle_width // 1.75, 10))
        for i in range(len(Visualisation.people_unit_list)):
            pygame.draw.circle(win, Visualisation.people_unit_list[i][0],
                               (Visualisation.people_unit_list[i][1][0], Visualisation.people_unit_list[i][1][1]),
                               Visualisation.UNIT_CIRCLE_RADIUS)

        # --------------------------------CZAS------------------------------------------------#
        # Rysowanie ramki dla dolnej części (czasu)
        time_surface = time_font.render("ITERACJA:", True, Visualisation.WHITE)
        win.blit(time_surface, (Visualisation.LEGEND_WIDTH // 2 - title_surface.get_width() // 1.5,
                                Visualisation.MAIN_HEIGHT + 0.1 * Visualisation.TIME_HEIGHT))

        iterator_surface = time_font.render(f"{Visualisation.year_iterator}", True, Visualisation.WHITE)
        win.blit(iterator_surface, (Visualisation.LEGEND_WIDTH // 2 - title_surface.get_width() // 5,
                                    Visualisation.MAIN_HEIGHT + 0.45 * Visualisation.TIME_HEIGHT))

        # Rysowanie paska ładowania
        for i in range(Visualisation.LEGEND_WIDTH, int(Visualisation.LOADING_PART * Visualisation.TIME_WIDTH)):
            pygame.draw.line(win, Visualisation.WHITE, (i, Visualisation.LEGEND_HEIGHT + Visualisation.TIME_HEIGHT // 4),
                             (i, Visualisation.LEGEND_HEIGHT + (Visualisation.TIME_HEIGHT // 4) * 3))

        # Zwiększenie paska ładowania
        Visualisation.LOADING_PART += 0.0015
        Visualisation.month_iterator += 1

        if Visualisation.month_iterator > 12:
            Visualisation.month_iterator = 1
            Visualisation.year_iterator += 1

        if Visualisation.LOADING_PART > 1:
            Visualisation.LOADING_PART = 0.1

        pygame.display.flip()
        pygame.time.wait(20)
