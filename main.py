import pygame
import sys

FRAME_COLOR = (0, 255, 204)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)

SIZE_BLOCK = 20
COUNT_BLOCKS = 30
MARGIN = 1
HEADER_MARGIN = 70

size = [
    SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
    SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS +
    HEADER_MARGIN
]

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake game')
timer = pygame.time.Clock()


class SnakeBlock:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS


def draw_block(color, row, col):
    pygame.draw.rect(screen, color, [
        SIZE_BLOCK + col * SIZE_BLOCK + MARGIN *
        (col + 1), HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN *
        (row + 1), SIZE_BLOCK, SIZE_BLOCK
    ])


if __name__ == '__main__':
    middle_of_field = COUNT_BLOCKS // 2
    snake_blocks = [
        SnakeBlock(middle_of_field, middle_of_field - 1),
        SnakeBlock(middle_of_field, middle_of_field),
        SnakeBlock(middle_of_field, middle_of_field + 1)
    ]

    d_row = 0
    d_col = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Exit')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        for row in range(COUNT_BLOCKS):
            for col in range(COUNT_BLOCKS):
                if (row + col) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE

                draw_block(color, row, col)

        head = snake_blocks[0]
        if not head.is_inside():
            print('Game over')
            pygame.quit()
            sys.exit()

        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        snake_blocks.insert(0, new_head)
        snake_blocks.pop()

        pygame.display.flip()
        timer.tick(5)
