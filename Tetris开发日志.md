今天完成了俄罗斯方块的基础功能，包括：

1. 利用tkinter绘制前端页面
2. 随机生成不同形状不同颜色的俄罗斯方块
3. 实现了新的俄罗斯方块下降功能，对新生成的俄罗斯方块可以进行左右移动，向下快速下降，顺时间旋转
4. 实现了得分和消除功能



对于代码的理解：

目前将代码分成了main.py 和basic.py 两个文件

main.py用于游戏循环内容的实现

basic.py 用于存储帮助函数

争取在学习的过程中实践解耦的思想



首先解读basic.py文件:

设置Roll Column cell_size 参数

参数解读：

+ block_list 记录每一行每一列的矩阵类型
+ Column Roll 分别是列和行
+ SHAPESCOLOR 是俄罗斯方块的颜色
+ SHAPES 是俄罗斯方块的相对位置
+ global current_block 当前俄罗斯方块
+ is_suspend 暂停bool

函数解读：

+ draw_cell_by_cr 函数 调用情况：对于每一个需要绘制格子的地方都会调用 操作：对每一个矩阵进行渲染，并携带tag
+ draw_board 函数 调用情况：只有在第一次初始化和达成得分条件（一行已满）的时候才会调用；操作：首先按行删除所有带有rowtag的格子，重新绘制canvas画布上所有rowtag的格子，如果是第一次调用，就绘制背景色格子
+ draw_cell 函数 调用情况：绘制指定形状指定颜色的俄罗斯方块，也就是正在下落的俄罗斯方块；操作：根据cell_list（即不同俄罗斯方块的相对位置）,判断每一个格子的行列是否在canvas中，调用draw_cell_by_cr函数绘制每一个格子,tag 为falling
+ draw_block_move 函数 调用情况：绘制俄罗斯方块的移动 操作： 提取出传入block的三个参数,先删除带有falling tag的格子，对cr进行修改,对block进行参数修改，重新绘制格子
+ generate_new_block 函数 调用情况： 在game_loop中循环调用，只要上一个方块停止了，就再次调用这个函数来生成新的俄罗斯方块 操作：设置block是从SHAPES.keys()中随机调用的，cr分别是[Column//2,0]，设置并返回new_block结构体{'kind''cell_list''cr'}
+ check_move 函数 调用情况：在每一个game_loop进行调用，检查block是否碰到了底部/是否超出了左右列 & 是否碰到了其他的方块(ri>0 and block_list[ri][ci]) 操作：提取参数，计算是否满足移动条件（参考draw_block_move的操作），返回bool值（感觉两个函数应该能合在一起
+ save_to_block_list 函数 调用情况：在game_loop中 当check_move返回False时，也就是方块不能动的时候，调用此函数来保存所有沉到底部的格子 操作：首先删除带有falling tag的格子，提取参数，对于俄罗斯方块的每一个格子参数保存至block_list并重新设置tag为row
+ horizontal_move_block 函数 调用情况 ：当按左右移动的时候调用 操作：检查current_block是否为None和是否可以继续向下移动, 如果True就在这一个game_loop中修改draw_block_move 的direction
+ rotate_block 函数 调用情况：当按UP键旋转当前的俄罗斯方块 操作：首先检查current_block是否为None,然后提取出cr参数，对其进行旋转并返回rotate_block ，利用check_move 函数检查旋转后的rotate_block 是否可以移动，将原本的用灰色覆盖（感觉其实用canvas.delete删除就可以了）,重新绘制rotate_block
+ land 函数 调用情况：当按住down来快速下降时 操作：分别计算当前俄罗斯方块每一个格子到底部的距离，取其最小值，将俄罗斯方块draw_block_move 距离
+ check_row_complete 函数 调用情况：计分和清除的时候调用 操作： 对于row中的每一个cell检查他在block_list中的数值是否为空
+ check_and_clear 函数 调用情况：每一个game_loop中检查是否有满的情况 操作：如果满了，就依次将上一行的列表复制到下一行，对block_list的第一行绘制空白，最终重新绘制一遍canvas
+ suspend 函数 调用情况 ：按空格暂停 操作：对is_suspend取反
+ change_global_block 函数 调用情况：由于跨文件参数不共享，需要在main.py用module的形式来调用basic中的函数才能修改basic中的参数

关于main.py

函数解读：

+ game_loop 函数 调用情况：游戏的运行主函数 操作：递归调用game_loop ,win.update启动tkinter窗口，首先判断current_block是否为None，如果是，生成新的block，draw_block_move,保存block值到current_block 再检查是否能移动，不能的话就显示游戏结束；如果current_block不是None就检查是否能移动，如果能就移动，不能就保存值到block_list并设current_block为空，之后检查计分和消除; win.after(FPS,game_loop)在FPS(ms)后调用本身，再次进入game_loop直到game_over

