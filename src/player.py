# Настройка персонажа (человечек)
player_width = 37
player_height = 50
player_x = 50
player_y = screen_height - player_height - 50
player_y_velocity = 0
gravity = 1
jump_power = -21
is_jumping = False

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
 # Рисование персонажа
    if not game_over and not show_skins:
        draw_player(player_x, player_y, skins[current_skin])
