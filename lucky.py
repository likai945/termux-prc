

import pygame, sys, random,copy
from pygame.locals import *


# 定义颜色
pinkColor = pygame.Color(255, 182, 193)
headColor = pygame.Color(223, 100, 233)
blackColor = pygame.Color(0, 0, 0)
whiteColor = pygame.Color(255, 255, 255)
luckyColor = pygame.Color(125, 25, 2)


# 定义游戏结束的函数
def gameover():
    pygame.quit()
    sys.exit()

def fruit(snk):
    isDiamond=random.randint(0,9)
    while True:
        x = random.randint(1, 31)
        y = random.randint(1, 23)
        foodPostion = [x*20,y*20]
        if foodPostion not in snk:
            return foodPostion,isDiamond

def init_snake():
    isVertical=random.randint(0,1)
    isPositive=random.randint(0,1)
    posline=random.randint(11,20)
    posdot=random.randint(11,17)
    if isVertical:
        x=posline
        snakeSegments = [[x*20,y*20] for y in range(posdot,posdot+4)]
        if isPositive:
            direction = 'up'
        else:
            direction = 'down'
            snakeSegments.reverse()
    else:
        y=posline
        snakeSegments = [[x*20,y*20] for x in range(posdot,posdot+4)]
        if isPositive:
            direction = 'right'
            snakeSegments.reverse()
        else:
            direction = 'left'
    return snakeSegments,direction


def main():
    # 初始化
    pygame.init()
    # 定义一个变量来控制速度
    time_clock = pygame.time.Clock()

    # 创建窗口，定义标题
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("贪吃蛇")

    # 定义蛇的初始化变量
    # 定义一个贪吃蛇的长度列表，其中有几个元素就代表有几段身体
    snake=init_snake()
    snakePosition = copy.deepcopy(snake[0][0])  # 蛇头位置
    snakeSegments = snake[0]
    last = copy.deepcopy(snake[0][-1])  
    oscore=0
    # 初始化食物位置
    food=fruit(snakeSegments)
    foodPostion=food[0]
    foodLucky=0
    # 食物数量，1是没被吃，0是被吃了
    foodTotal = 1
    # 初始方向，向右
    direction = snake[1]
    # 定义一个改变方向的变量，按键
    changeDirection = direction

    # 通过键盘控制蛇的运动
    while True:
        # 从队列中获取事件
        for event in pygame.event.get():
            # 判断是否为退出事件
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # 按键事件
            elif event.type == KEYDOWN:
                # 如果是右键头或者是d，蛇向右移动
                if event.key == K_RIGHT or event.key == K_d:
                    changeDirection = 'right'
                # 如果是左键头或者是a，蛇向左移动
                if event.key == K_LEFT or event.key == K_a:
                    changeDirection = 'left'
                if event.key == K_UP or event.key == K_w:
                    changeDirection = 'up'
                if event.key == K_DOWN or event.key == K_s:
                    changeDirection = 'down'
                # 对应键盘上的Esc键，表示退出
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))

        # 确认方向，判断是否输入了反方向运动
        if changeDirection == 'right' and not direction == 'left':
            direction = changeDirection
        if changeDirection == 'left' and not direction == 'right':
            direction = changeDirection
        if changeDirection == 'up' and not direction == 'down':
            direction = changeDirection
        if changeDirection == 'down' and not direction == 'up':
            direction = changeDirection

        # 根据方向移动蛇头
        if direction == 'right':
            snakePosition[0] += 20
        if direction == 'left':
            snakePosition[0] -= 20
        if direction == 'up':
            snakePosition[1] -= 20
        if direction == 'down':
            snakePosition[1] += 20

        # 增加蛇的长度
        snakeSegments.insert(0, list(snakePosition))
        # 判断是否吃到食物
        if snakePosition == foodPostion:
            foodTotal = 0
            if foodLucky == 9:
                snakeSegments.append(last)
        else:
            last=snakeSegments.pop()  # 每次将最后一单位蛇身剔除列表

        # 如果食物为0 重新生成食物
        if foodTotal == 0:
            foodTotal=1
            food=fruit(snakeSegments)
            foodPostion=food[0]
            foodLucky=food[1]


        # 绘制pygame显示层
        screen.fill(blackColor)


        for position in snakeSegments[1:]:  # 蛇身为白色
            # 化蛇
            pygame.draw.rect(screen, headColor, Rect(snakePosition[0], snakePosition[1], 20, 20))
            pygame.draw.rect(screen, pinkColor, Rect(position[0], position[1], 20, 20))
            if foodLucky==9:
                pygame.draw.rect(screen, luckyColor, Rect(foodPostion[0], foodPostion[1], 20, 20))
            else:
                pygame.draw.rect(screen, whiteColor, Rect(foodPostion[0], foodPostion[1], 20, 20))

        # 更新显示到屏幕表面
        pygame.display.flip()

        # 判断游戏是否结束
        if snakePosition[0] > 620 or snakePosition[0] < 0:
            gameover()
        elif snakePosition[1] > 460 or snakePosition[1] < 0:
            gameover()
        # 如果碰到自己的身体
        if snakePosition in snakeSegments[1:]:
            gameover()

        # 控制游戏速度
        time_clock.tick(10)
        cscore=len(snakeSegments)-4
        if cscore>oscore:
            print(cscore)
            oscore=cscore



#  启动入口函数
if __name__ == '__main__':
    main()
