import sys
import pygame
import pygame_menu
from random import randint

FRAME_COLOR = (0, 255, 204)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
RED = (224, 0, 0)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)

SIZE_BLOCK = 20
COUNT_BLOCKS = 20
MARGIN = 1
HEADER_MARGIN = 70
FONT_SIZE = 35
START_SPEED = 6

SIZE = [
    SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
    SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS +
    HEADER_MARGIN
]

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Snake game')


class SnakeBlock:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other) -> bool:
        return isinstance(
            other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color, row, col):
    pygame.draw.rect(screen, color, [
        SIZE_BLOCK + col * SIZE_BLOCK + MARGIN *
        (col + 1), HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN *
        (row + 1), SIZE_BLOCK, SIZE_BLOCK
    ])


def start_the_game():

    def get_random_empty_block():
        x = randint(0, COUNT_BLOCKS - 1)
        y = randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = randint(0, COUNT_BLOCKS - 1)
            empty_block.y = randint(0, COUNT_BLOCKS - 1)

        return empty_block

    timer = pygame.time.Clock()
    courier_font = pygame.font.SysFont('Courier', FONT_SIZE)

    middle_of_field = COUNT_BLOCKS // 2
    snake_blocks = [
        SnakeBlock(middle_of_field, middle_of_field - 1),
        SnakeBlock(middle_of_field, middle_of_field),
        SnakeBlock(middle_of_field, middle_of_field + 1)
    ]

    apple = get_random_empty_block()
    pos_row = 0
    pos_col = -1
    total_score = 0
    snake_speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and pos_col != 0:
                    pos_row = -1
                    pos_col = 0
                elif event.key == pygame.K_DOWN and pos_col != 0:
                    pos_row = 1
                    pos_col = 0
                elif event.key == pygame.K_LEFT and pos_row != 0:
                    pos_row = 0
                    pos_col = -1
                elif event.key == pygame.K_RIGHT and pos_row != 0:
                    pos_row = 0
                    pos_col = 1

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, SIZE[0], HEADER_MARGIN])

        total_score_text = courier_font.render(f'Total: {total_score}', 0,
                                               WHITE)
        snake_speed_text = courier_font.render(f'Speed: {snake_speed}', 0,
                                               WHITE)
        screen.blit(total_score_text, (2 * SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(snake_speed_text,
                    (SIZE_BLOCK + SIZE[0] // 2 + 4 * SIZE_BLOCK, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for col in range(COUNT_BLOCKS):
                if (row + col) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE

                draw_block(color, row, col)

        head = snake_blocks[0]
        if not head.is_inside():
            break

        draw_block(RED, apple.x, apple.y)

        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        pygame.display.flip()

        if apple == head:
            total_score += 1
            snake_speed = total_score // 7 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        new_head = SnakeBlock(head.x + pos_row, head.y + pos_col)
        if new_head in snake_blocks:
            break

        snake_blocks.insert(0, new_head)
        snake_blocks.pop()

        timer.tick(START_SPEED + snake_speed)


if __name__ == '__main__':
    pygame.init()

    menu = pygame_menu.Menu('Welcome',
                            SIZE[0],
                            SIZE[1],
                            theme=pygame_menu.themes.THEME_BLUE)

    menu.add.text_input('Name :', default='Player1')
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)