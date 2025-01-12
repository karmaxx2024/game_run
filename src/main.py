import sys
import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройка экрана
screen_width = 900
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('runner')

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
brown = (139, 69, 19)  # Цвет коричневый для крыши
gray = (128, 128, 128)  # Цвет асфальта
light_blue = (173, 216, 230)  # Цвет для облаков
skin_color = (255, 224, 189)  # Цвет кожи для человечка

# Настройка частоты обновления экрана
clock = pygame.time.Clock()

# Настройка персонажа (человечек)
player_width = 37
player_height = 50
player_x = 50
player_y = screen_height - player_height - 50
player_y_velocity = 0
gravity = 1
jump_power = -21
is_jumping = False

# Препятствие (камень)
obstacle_width = 40
obstacle_height = 40
obstacle_x = screen_width
obstacle_y = screen_height - obstacle_height - 50
obstacle_speed = 7

# Большой камень
big_rock_width = 55  # Увеличенный размер
big_rock_height = 55
big_rock_x = screen_width
big_rock_y = screen_height - big_rock_height - 50
big_rock_speed = 5  # Увеличенная скорость

# Машина
car_width = 70
car_height = 50
car_x = screen_width
car_y = screen_height - car_height - 50
car_speed = 8
car_spawn_delay = 265  # Задержка появления машины (в кадрах)
car_spawn_counter = 0  # Счетчик для задержки

# Облака
cloud_width = 100
cloud_height = 50
clouds = []
for _ in range(5):
    cloud_x = random.randint(0, screen_width)
    cloud_y = random.randint(0, screen_height // 4)
    clouds.append((cloud_x, cloud_y))

# Поезд
train_width = 150
train_height = 50
train_x = screen_width
train_y = screen_height - train_height - 100
train_speed = 10
train_spawn_delay = 50  # Задержка появления поезда (в кадрах)
train_spawn_counter = 0  # Счетчик для задержки

def draw_train(x, y):
    # Основной корпус поезда
    pygame.draw.rect(screen, (0, 0, 255), (x, y, train_width, train_height))  # Синий поезд
    # Окна
    pygame.draw.rect(screen, white, (x + 10, y + 10, 30, 20))
    pygame.draw.rect(screen, white, (x + 50, y + 10, 30, 20))
    # Колеса
    pygame.draw.circle(screen, black, (x + 20, y + train_height), 10)
    pygame.draw.circle(screen, black, (x + train_width - 20, y + train_height), 10)

def draw_railway_tracks():
    # Шпалы
    sleeper_width = 100
    sleeper_height = 10
    sleeper_spacing = 50
    for i in range(0, screen_width, sleeper_spacing):
        pygame.draw.rect(screen, (139, 69, 19), (i, screen_height - 70, sleeper_width, sleeper_height))  # Коричневые шпалы

    # Рельсы
    rail_width = screen_width
    rail_height = 5
    pygame.draw.rect(screen, gray, (0, screen_height - 80, rail_width, rail_height))  # Левый рельс
    pygame.draw.rect(screen, gray, (0, screen_height - 60, rail_width, rail_height))  # Правый рельс

def draw_semaphore(x, y):
    # Основание семафора
    pygame.draw.rect(screen, gray, (x, y, 10, 50))  # Стойка
    pygame.draw.circle(screen, red, (x + 5, y + 10), 5)  # Красный сигнал
    pygame.draw.circle(screen, green, (x + 5, y + 30), 5)  # Зеленый сигнал

def draw_railway_sign(x, y, text):
    # Основание знака
    pygame.draw.rect(screen, gray, (x, y, 30, 50))
    # Текст на знаке
    sign_font = pygame.font.Font(None, 24)
    sign_text = sign_font.render(text, True, black)
    screen.blit(sign_text, (x + 5, y + 20))

def draw_smoke(x, y):
    pygame.draw.circle(screen, (200, 200, 200), (x, y), 10)  # Дым
    pygame.draw.circle(screen, (220, 220, 220), (x + 10, y - 10), 8)
    pygame.draw.circle(screen, (240, 240, 240), (x + 20, y - 20), 6)

# Счет
score = 0
high_score = 0
font = pygame.font.Font(None, 36)

# Уровни и скины
levels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # Очки для перехода на следующий уровень
unlocked_skins = [0]  # Начальный скин разблокирован
current_level = 0
current_skin = 0  # Индекс текущего скина

# Скины
skins = [
    (255, 224, 189),  # Светлый
    (210, 180, 140),  # Тан
    (139, 69, 19),    # Коричневый
    (255, 0, 0),      # Красный
    (0, 255, 0),      # Зеленый
    (0, 0, 255),      # Синий
    (255, 255, 0),    # Желтый
    (255, 0, 255),    # Пурпурный
    (0, 255, 255),    # Голубой
    (128, 0, 128)     # Фиолетовый
]

# Функция для загрузки рекорда из файла
def load_high_score():
    try:
        with open("../data/high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Функция для сохранения рекорда в файл
def save_high_score(score):
    with open("../data/high_score.txt", "w") as file:
        file.write(str(score))

# Загрузка рекорда
high_score = load_high_score()

# Функция для рисования дома
def draw_house(x, y, width, height, color):
    # Основание дома (квадрат)
    pygame.draw.rect(screen, color, (x, y, width, height))

    # Крыша (треугольник)
    roof_points = [
        (x, y),
        (x + width // 2, y - 50),
        (x + width, y)
    ]
    pygame.draw.polygon(screen, brown, roof_points)

    # Окно (квадрат)
    window_width = 30
    window_height = 30
    window_x = x + width // 4
    window_y = y + height // 4
    pygame.draw.rect(screen, blue, (window_x, window_y, window_width, window_height))

    # Дверь
    door_width = 30
    door_height = 60
    door_x = x + width // 2 - door_width // 2
    door_y = y + height - door_height
    pygame.draw.rect(screen, brown, (door_x, door_y, door_width, door_height))

# Функция для рисования облака
def draw_cloud(x, y):
    pygame.draw.ellipse(screen, light_blue, (x, y, cloud_width, cloud_height))
    pygame.draw.ellipse(screen, light_blue, (x + 30, y - 20, cloud_width, cloud_height))
    pygame.draw.ellipse(screen, light_blue, (x + 60, y, cloud_width, cloud_height))

# Функция для рисования дерева
def draw_tree(x, y):
    # Ствол дерева
    pygame.draw.rect(screen, (139, 69, 19), (x, y, 20, 100))  # Коричневый ствол
    # Крона дерева (темно-зеленый круг)
    pygame.draw.circle(screen, (0, 100, 0), (x + 10, y - 30), 50)  # Темно-зеленая крона

# Функция для рисования машины
def draw_car(x, y):
    pygame.draw.rect(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (x, y, car_width, car_height))
    pygame.draw.circle(screen, black, (x + 20, y + car_height), 15)
    pygame.draw.circle(screen, black, (x + car_width - 20, y + car_height), 15)

# Функция для рисования человечка
def draw_player(x, y, skin):
    # Голова
    pygame.draw.circle(screen, skin, (x + player_width // 2, y - 20), 20)
    # Тело
    pygame.draw.rect(screen, black, (x + player_width // 2 - 10, y, 20, player_height))
    # Ноги
    pygame.draw.line(screen, black, (x + player_width // 2 - 10, y + player_height), (x, y + player_height + 30), 5)
    pygame.draw.line(screen, black, (x + player_width // 2 + 10, y + player_height), (x + player_width, y + player_height + 30), 5)
    # Руки
    pygame.draw.line(screen, black, (x + player_width // 2 - 10, y + 20), (x - 10, y + 40), 5)
    pygame.draw.line(screen, black, (x + player_width // 2 + 10, y + 20), (x + player_width + 10, y + 40), 5)

# Функция для отображения меню скинов
def show_skins_menu():
    screen.fill(white)
    skin_font = pygame.font.Font(None, 48)
    title_text = skin_font.render("Выберите скин", True, black)
    screen.blit(title_text, (screen_width // 2 - 100, 50))

    for i, skin in enumerate(skins):
        skin_rect = pygame.Rect(100 + (i % 5) * 200, 200 + (i // 5) * 200, 150, 150)
        if i in unlocked_skins:
            pygame.draw.rect(screen, skin, skin_rect)
        else:
            pygame.draw.rect(screen, gray, skin_rect)
        if skin_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, black, skin_rect, 3)

    pygame.display.flip()

# Функция для рисования карты
def draw_map(level):
    if level == 0:
        # Город
        screen.fill(white)
        pygame.draw.rect(screen, gray, (0, screen_height - 50, screen_width, 50))  # Асфальт
        # Рисуем дома
        house_colors = [red, green, blue, (255, 165, 0), (128, 0, 128), (0, 128, 128), (255, 215, 0), (255, 192, 203)]
        house_width = 100
        house_height = 120
        house_spacing = 20  # Расстояние между домами

        for i in range(8):  # Рисуем 8 домов
            house_x = 50 + i * (house_width + house_spacing)
            house_y = screen_height // 2 - house_height // 2
            draw_house(house_x, house_y, house_width, house_height, house_colors[i])
    elif level == 1:
        # Джунгли
        screen.fill((34, 139, 34))  # Зеленый цвет
        pygame.draw.rect(screen, (139, 69, 19), (0, screen_height - 50, screen_width, 50))  # Коричневый цвет
        # Рисуем деревья
        draw_tree(100, screen_height - 150)
        draw_tree(300, screen_height - 150)
        draw_tree(500, screen_height - 150)
        draw_tree(700, screen_height - 150)
        draw_tree(900, screen_height - 150)
    elif level == 2:
        # Железнодорожные пути
        screen.fill((105, 105, 105))  # Серый цвет
        pygame.draw.rect(screen, (0, 0, 0), (0, screen_height - 50, screen_width, 50))  # Черный цвет
        # Рисуем рельсы и шпалы
        draw_railway_tracks()
        # Рисуем семафоры
        draw_semaphore(100, screen_height - 150)
        draw_semaphore(screen_width - 150, screen_height - 150)
        # Рисуем знаки
        draw_railway_sign(200, screen_height - 200, "STOP")
        draw_railway_sign(screen_width - 250, screen_height - 200, "GO")
        # Рисуем поезд
        if train_spawn_counter >= train_spawn_delay:
            draw_train(train_x, train_y)
    elif level == 3:
        # Зима (домики эльфов и деда мороза)
        screen.fill((173, 216, 230))  # Голубой цвет
        pygame.draw.rect(screen, (255, 250, 250), (0, screen_height - 50, screen_width, 50))  # Белый цвет
    elif level == 4:
        # Библиотека
        screen.fill((210, 180, 140))  # Тан цвет
        pygame.draw.rect(screen, (139, 69, 19), (0, screen_height - 50, screen_width, 50))  # Коричневый цвет
    elif level == 5:
        # Школа
        screen.fill((255, 223, 186))  # Бежевый цвет
        pygame.draw.rect(screen, (128, 0, 0), (0, screen_height - 50, screen_width, 50))  # Темно-красный цвет
    elif level == 6:
        # Стадион
        screen.fill((0, 100, 0))  # Темно-зеленый цвет
        pygame.draw.rect(screen, (192, 192, 192), (0, screen_height - 50, screen_width, 50))  # Серебряный цвет
    elif level == 7:
        # Торговый центр
        screen.fill((255, 255, 0))  # Желтый цвет
        pygame.draw.rect(screen, (128, 128, 128), (0, screen_height - 50, screen_width, 50))  # Серый цвет
    elif level == 8:
        # Зоопарк
        screen.fill((0, 255, 0))  # Зеленый цвет
        pygame.draw.rect(screen, (139, 69, 19), (0, screen_height - 50, screen_width, 50))  # Коричневый цвет
    elif level == 9:
        # Больница
        screen.fill((255, 255, 255))  # Белый цвет
        pygame.draw.rect(screen, (255, 0, 0), (0, screen_height - 50, screen_width, 50))  # Красный цвет


# Основной цикл
running = True
game_over = False
show_skins = False

is_on_train = False  # Переменная для отслеживания, находится ли персонаж на поезде

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_skins:
                for i, skin in enumerate(skins):
                    skin_rect = pygame.Rect(100 + (i % 5) * 200, 200 + (i // 5) * 200, 150, 150)
                    if skin_rect.collidepoint(event.pos) and i in unlocked_skins:
                        current_skin = i
                        show_skins = False
            elif 'skins_button_rect' in locals() and skins_button_rect.collidepoint(event.pos):
                show_skins = True
            elif game_over:
                # Обработка нажатия на кнопку "Начать заново"
                restart_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 20, 200, 60)
                if restart_button_rect.collidepoint(event.pos):
                    # Сброс игры
                    game_over = False
                    score = 0
                    player_x = 50
                    player_y = screen_height - player_height - 50
                    player_y_velocity = 0
                    obstacle_x = screen_width
                    big_rock_x = screen_width
                    car_x = screen_width
                    car_spawn_counter = 0
                    current_level = 0
                    unlocked_skins = [0]
                    current_skin = 0
                    is_on_train = False

    # Управление персонажем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping and not game_over and not show_skins:
        if is_on_train:
            player_y_velocity = jump_power  # Прыжок с поезда
            is_on_train = False
        else:
            player_y_velocity = jump_power  # Обычный прыжок
        is_jumping = True

    # Гравитация
    if not game_over and not show_skins:
        if not is_on_train:
            player_y_velocity += gravity
            player_y += player_y_velocity

    # Проверка, если персонаж приземлился
    if player_y >= screen_height - player_height - 50 and not is_on_train:
        player_y = screen_height - player_height - 50
        is_jumping = False

    # Проверка нахождения на поезде
    if (player_x + player_width > train_x and
        player_x < train_x + train_width and
        player_y + player_height >= train_y and
        player_y + player_height <= train_y + 10):  # 10 - это небольшой зазор для точности
        is_on_train = True
        player_y = train_y - player_height  # Фиксируем позицию персонажа на поезде
    else:
        is_on_train = False

    # Движение персонажа на поезде
    if is_on_train:
        player_x += train_speed  # Персонаж движется вместе с поездом

    # Движение препятствий
    if not game_over and not show_skins:
        obstacle_x -= obstacle_speed
        if obstacle_x + obstacle_width < 0:
            obstacle_x = screen_width
            score += 1

        big_rock_x -= big_rock_speed
        if big_rock_x + big_rock_width < 0:
            big_rock_x = screen_width
            score += 1

        # Появление машины с задержкой (только на уровне 0)
        if current_level == 0:
            car_spawn_counter += 1
            if car_spawn_counter >= car_spawn_delay:
                car_x -= car_speed
                if car_x + car_width < 0:
                    car_x = screen_width
                    car_spawn_counter = 0
                    score += 1

        # Появление поезда с задержкой (только на уровне 2)
        if current_level == 2:
            train_spawn_counter += 1
            if train_spawn_counter >= train_spawn_delay:
                train_x -= train_speed
                if train_x + train_width < 0:
                    train_x = screen_width
                    train_spawn_counter = 0
                    score += 1

    # Проверка столкновения
    if not game_over and not show_skins:
        # Столкновение с камнем (только если не на поезде)
        if not is_on_train and (player_x + player_width > obstacle_x and
                                player_x < obstacle_x + obstacle_width and
                                player_y + player_height > obstacle_y):
            game_over = True

        # Столкновение с большим камнем (только если не на поезде)
        if not is_on_train and (player_x + player_width > big_rock_x and
                                player_x < big_rock_x + big_rock_width and
                                player_y + player_height > big_rock_y):
            game_over = True

        # Столкновение с машиной (только на уровне 0 и если не на поезде)
        if current_level == 0 and not is_on_train and (player_x + player_width > car_x and
                                                       player_x < car_x + car_width and
                                                       player_y + player_height > car_y):
            game_over = True

    # Обновление рекорда
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    # Проверка уровня
    if current_level < len(levels) and score >= levels[current_level]:
        current_level += 1
        if current_level < len(skins):
            unlocked_skins.append(current_level)

    # Очистка экрана и рисование карты
    draw_map(current_level)

    # Рисование облаков
    for i in range(len(clouds)):
        cloud_x, cloud_y = clouds[i]
        draw_cloud(cloud_x, cloud_y)
        clouds[i] = (cloud_x - 1, cloud_y)  # Движение облаков
        if cloud_x + cloud_width < 0:
            clouds[i] = (screen_width, random.randint(0, screen_height // 4))

    # Рисование персонажа
    if not game_over and not show_skins:
        draw_player(player_x, player_y, skins[current_skin])

    # Рисование препятствий
    if not game_over and not show_skins:
        pygame.draw.rect(screen, red, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
        pygame.draw.rect(screen, brown, (big_rock_x, big_rock_y, big_rock_width, big_rock_height))
        # Машина появляется только на уровне 0
        if current_level == 0 and car_spawn_counter >= car_spawn_delay:
            draw_car(car_x, car_y)
        # Поезд появляется только на уровне 2
        if current_level == 2 and train_spawn_counter >= train_spawn_delay:
            draw_train(train_x, train_y)

    # Отображение счета
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    # Отображение рекорда
    high_score_text = font.render(f"High Score: {high_score}", True, black)
    screen.blit(high_score_text, (10, 50))

    # Отображение уровня
    level_text = font.render(f"Level: {current_level + 1}", True, black)
    screen.blit(level_text, (10, 90))

    # Кнопка "Скины"
    skins_button_rect = pygame.Rect(screen_width - 150, 10, 140, 40)
    pygame.draw.rect(screen, green, skins_button_rect)
    skins_text = font.render("Скины", True, black)
    screen.blit(skins_text, (screen_width - 140, 20))

    # Отображение экрана "Game Over"
    if game_over:
        # Черный фон
        screen.fill(black)

        # Текст "Game Over"
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, red)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        # Кнопка "Начать заново"
        restart_font = pygame.font.Font(None, 48)
        restart_text = restart_font.render("Начать заново", True, white)
        restart_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 20, 200, 60)
        pygame.draw.rect(screen, green, restart_button_rect)
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        screen.blit(restart_text, restart_text_rect)

    # Отображение меню скинов
    if show_skins:
        show_skins_menu()

    # Обновление экрана
    pygame.display.flip()

    # Управление частотой обновления экрана
    clock.tick(60)

# Завершение Pygame
pygame.quit()
sys.exit()