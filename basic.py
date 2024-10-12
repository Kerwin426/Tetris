import tkinter as tk
import random
cell_size = 15
Column = 18
Roll = 30
height = Roll*cell_size
width = Column*cell_size
FPS = 100


# 绘制单个格子
def draw_cell_by_cr(canvas,column,roll,color="#CCCCCC",tag_kind=""):
    
    x0 = column*cell_size
    y0 = roll*cell_size
    x1 = (column+1)*cell_size
    y1 = (roll+1)*cell_size
    # 给每一个格子打tag 分为falling(下降) 落地的格子(row) 其他空白格子
    if tag_kind=="falling":
        canvas.create_rectangle(x0,y0,x1,y1,fill = color,outline="white",width=2,tag=tag_kind)
    elif tag_kind=="row":
        canvas.create_rectangle(x0,y0,x1,y1,fill = color,outline="white",width=2,tag="row-%s"%roll)
    else:
        canvas.create_rectangle(x0,y0,x1,y1,fill = color,outline="white",width=2)

# 绘制canvas上所有的格子
def draw_board(canvas,block_list,isFirst=False):
    # 每一次绘制画板先删除所有的行
    for ri in range(Roll):
        canvas.delete("row-%s"%ri)
    # 再绘制新的格子
    for ri in range(Roll):
        for ci in range(Column):
            cell_type = block_list[ri][ci]
            if cell_type:
                draw_cell_by_cr(canvas,ci,ri,SHAPESCOLOR[cell_type],tag_kind="row")
            elif isFirst:
                # 对于背景色只在第一次进行绘制
                draw_cell_by_cr(canvas,ci,ri)

SHAPES = {
    "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)],
    "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],
    "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],
    "I": [(0, 1), (0, 0), (0, -1), (0, -2)],
    "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
    "J": [(-1, 0), (0, 0), (0, -1), (0, -2)]
}
 
SHAPESCOLOR = {
    "O": "blue",
    "Z": "Cyan",
    "S": "red",
    "T": "yellow",
    "I": "green",
    "L": "purple",
    "J": "orange",
}
# 绘制指定颜色指定形状的俄罗斯方块
def draw_cells(canvas,c,r,cell_list,color='#CCCCCC'):
    for cell in cell_list:
        cell_c ,cell_r = cell
        ci = cell_c+c
        ri = cell_r+r
        if 0<=c <Column and 0<=r<Roll:
            draw_cell_by_cr(canvas,ci,ri,color,tag_kind="falling")



win = tk.Tk()
score = 0
win.title("俄罗斯方块 SCORES: %s"% score)
win.resizable(False,False)

canvas  = tk.Canvas(win,width=width,height=height)
text = tk.Label(win,text='俄罗斯方块',bg="yellow")
Button_exit = tk.Button(win,text='退出',command=exit).pack(side='right')
text.pack(side="right")
canvas.pack()


block_list =[]
for i in range(Roll):
    i_row = ['' for j in range(Column)]
    block_list.append(i_row)



def draw_block_move(canvas,block,direction=[0,0]):
    shape_type = block['kind']
    cell_list = block['cell_list']
    c,r = block['cr']
    dc,dr = direction
    
    # 移动前，先清除原有位置绘制的俄罗斯方块
    canvas.delete("falling")

    new_c,new_r = c+dc,r+dr
    block['cr'] =[new_c,new_r]
    draw_cells(canvas,new_c,new_r,cell_list,SHAPESCOLOR[shape_type])

# 生成新的方块
def generate_new_block():
    block = random.choice(list(SHAPES.keys()))
    cr = [Column//2,0]
    new_block ={
        'kind':block,
        'cell_list':SHAPES[block],
        'cr':cr
    }
    return new_block

# 检查是否可以继续向direction方向移动
def check_move(block,direction=[0,0]):
    cell_list = block['cell_list']
    c,r = block['cr']
    for cell in cell_list:
        cell_c ,cell_r = cell
        ci = cell_c+c+direction[0]
        ri = cell_r+r+direction[1]
        if ci>=Column or ci<0 or ri>=Roll:
            return False
        if ri>=0 and block_list[ri][ci]:
            return False
    return True

# 记录每一格的shape_type 存入block_list
def save_to_block_list(block):
    canvas.delete("falling")
    cell_list = block['cell_list']
    c,r = block['cr']
    block_type = block['kind']
    for cell in cell_list:
        ci,ri = cell
        cc = c+ci
        rr = r+ri
        block_list[rr][cc]=block_type
        # 当方块落地后，需要修改tag
        draw_cell_by_cr(canvas,cc,rr,SHAPESCOLOR[block_type],tag_kind="row")

# 左右移动
def horizontal_move_block(event):
    print("Left or Right key pressed")
    direction = [0,0]
    if event.keysym =='Left':
        direction = [-1,0]
    elif event.keysym=='Right':
        direction = [1,0]
    else:
        return
    
    global current_block
    if current_block is not None and check_move(current_block,direction):
        draw_block_move(canvas,current_block,direction)

# 按UP键旋转
def rotate_block(event):
    print("Up key pressed")
    global current_block
    if current_block is None:
        return
    cell_list = current_block['cell_list']
    rotate_block = []
    for cell in cell_list:
        ci,ri = cell
        rotate_cell = [ri,-ci]
        rotate_block.append(rotate_cell)
    block_after_rotate ={
        'kind':current_block['kind'],
        'cell_list':rotate_block,
        'cr':current_block['cr']
    }
    if  check_move(block_after_rotate):
        cc,cr = current_block['cr']
        draw_cells(canvas,cc,cr,current_block["cell_list"])
        draw_cells(canvas,cc,cr,rotate_block,SHAPESCOLOR[current_block["kind"]])
        current_block = block_after_rotate

#按Down快速下降
def land(event):
    print("Down key pressed")
    global current_block
    if current_block is None:
        return
    cell_list = current_block["cell_list"]
    cc,cr = current_block["cr"]
    min_height = Roll
    for cell in cell_list:
        ci,ri = cell
        c = cc+ci
        r = cr+ri
        if block_list[r][c]:
            return
        h=0
        for ri in range(r+1,Roll):
            if block_list[ri][c]:
                break
            else:
                h+=1
        if h<min_height:
            min_height = h
    down =[0,min_height]
    if check_move(current_block,down):
        draw_block_move(canvas,current_block,down)            

# 检查行是否满的帮助函数
def check_row_complete(row):
    for cell in row:
        if cell=='':
            return False
    return True

# 计分和清除函数
def check_and_clear():
    has_completed_row = False
    for ri in range(len(block_list)):
        if check_row_complete(block_list[ri]):
            has_completed_row = True
            if ri>0:
                for cur_ri in range(ri,0,-1):
                    block_list[cur_ri] = block_list[cur_ri-1][:]
                block_list[0] = [''for j in range(Column)]
            else:
                block_list[ri] = [''for j in range(Column)]
            global score
            score+=10
    if has_completed_row:
        draw_board(canvas,block_list)
        win.title("SCORE: %s" %score)


def suspend(event):
    print("Space key pressed")
    global is_suspend
    is_suspend = not is_suspend

def change_global_block(block):
    global current_block
    current_block = block


current_block = None
is_suspend = False

canvas.focus_set()
canvas.bind("<KeyPress-Left>",horizontal_move_block)
canvas.bind("<KeyPress-Right>",horizontal_move_block)
canvas.bind("<KeyPress-Up>",rotate_block)
canvas.bind("<KeyPress-Down>",land)
canvas.bind("<space>",suspend)