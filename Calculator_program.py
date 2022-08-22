import pygame

class Button():
    def __init__(self, position, width, height, description, colour):
        self.position = position
        self.description = description
        self.width = width
        self.height = height
        self.colour = colour

    def display(self, screen, text_font):
        pygame.draw.rect(screen, self.colour, (self.position[0], self.position[1], self.width, self.height))
        text_surface = text_font.render(self.description, False, (255,255,255))
        screen.blit(text_surface, self.position)

    def get_description(self):
        return self.description

class NumberDisplay():
    def __init__(self, position, width, height, colour):
        self.position = position
        self.width = width
        self.height = height
        self.characters = []
        self.colour = colour

    def add_character(self, character):
        self.characters.append(character)

    def display(self, screen, text_font):
        text_characters = ""
        for character in self.characters:
            text_characters += character
        pygame.draw.rect(screen, self.colour, (self.position[0], self.position[1], self.width, self.height))
        text_surface = text_font.render(text_characters, False, (255,255,255))
        screen.blit(text_surface, self.position)

    def to_reverse_polish_notation(self):
        symbols = ['x', '/',  '+', '-', '=']

        reverse_polish_notation = []
        operators = []
        higher_priority = False

        for character in self.characters:
            if character not in symbols:
                reverse_polish_notation.append(character)
                if higher_priority == True:
                    reverse_polish_notation.append(operators[-1])
                    operators.remove(operators[-1])
                    higher_priority = False
            else:
                if character == '/' or character == 'x':
                    operators.append(character)
                    higher_priority = True
                elif character == '+' or character == '-':
                    if len(operators) == 0:
                        operators.append(character)
                    else:
                        reverse_polish_notation.append(operators.pop())
                        operators.append(character)

        if len(operators) != 0:
            reverse_polish_notation.append(operators[0])

        return reverse_polish_notation

    def calculate(self):
        symbols = ['x', '/',  '+', '-', '=']
        rpn_list = self.to_reverse_polish_notation()
        stack = []

        for i in range(0, len(rpn_list)):
            if rpn_list[i] not in symbols:
                stack.append(float(rpn_list[i]))
            elif rpn_list[i] in symbols:
                if rpn_list[i] == '+':
                    stack.append(stack.pop() + stack.pop())
                elif rpn_list[i] == '-':
                    temp_num = stack.pop()
                    stack.append(stack.pop() - temp_num)
                elif rpn_list[i] == 'x':
                    stack.append(stack.pop() * stack.pop())
                elif rpn_list[i] == '/':
                    temp_num = stack.pop()
                    stack.append(stack.pop() / temp_num)
            print(stack)
        self.characters = []
        self.characters.append(str(stack[0]))

        return stack[0]

def main():
    pygame.font.init()
    text_font = pygame.font.SysFont('Calibri', 30)

    screen_size = (500, 700)
    screen = pygame.display.set_mode(screen_size)
    background_colour = (240, 240, 240)
    pygame.display.set_caption("Calculator")
    screen.fill(background_colour)

    button_colour = (15, 15, 15)
    buttons = []
    index = 1

    number_display = NumberDisplay([0,0], int(screen_size[0]), int(screen_size[1]*0.2), button_colour)

    for i in range(1,4):
        for j in range(0,3):
            buttons.append(Button([screen_size[0]*(j/4), screen_size[1]*(i/4)], int(screen_size[0]/5), int(screen_size[1]/6), f"{index}", button_colour))
            index += 1

    symbols = ['CE', 'x', '/',  '+', '-', '=']

    size_index = 1
    for i in range (1,len(symbols)+1):
        buttons.append(Button([screen_size[0]*0.75, screen_size[1]*(size_index/4)], int(screen_size[0]/5), int(screen_size[1]/10), symbols[i-1], button_colour))
        size_index += 0.5

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for button in buttons:
            button.display(screen, text_font)

        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if pos[0] >= button.position[0] and pos[1] >= button.position[1] and pos[0] <= button.position[0]+button.width and pos[1] <= button.position[1]+button.height:
                        if button.get_description() != '=':
                            if button.get_description() == 'CE':
                                number_display.characters = []
                            else:
                                number_display.add_character(button.get_description())
                        else:
                            print(number_display.to_reverse_polish_notation())
                            print(number_display.calculate())

        number_display.display(screen, text_font)
        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

main()

