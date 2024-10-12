from tkinter import messagebox
from basic import FPS,win,canvas
from basic import draw_board,draw_block_move,generate_new_block,check_and_clear,check_move,save_to_block_list,change_global_block
import basic


# 第一次绘制画板，这里设置为True
draw_board(canvas,basic.block_list,True)


def game_loop():
    win.update()
    down = [0,1]
    if not basic.is_suspend:
        if basic.current_block is None:
            new_block = generate_new_block()
            draw_block_move(canvas,new_block)
            change_global_block(new_block)
            if not check_move(basic.current_block):
                messagebox.showinfo("Game Over :","Your score is %s" % basic.score)
                win.destroy()
                return
        else:
            if check_move(basic.current_block,down):
                draw_block_move(canvas,basic.current_block,down)
            else:
                save_to_block_list(basic.current_block)
                change_global_block(None)
    check_and_clear()
    win.after(FPS,game_loop)

game_loop()
win.mainloop()