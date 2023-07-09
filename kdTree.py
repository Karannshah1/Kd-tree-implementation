import random
import tkinter as tk
import matplotlib.pyplot as plt

pointxy = []


class Node:
    def __init__(self, point, split_dim, left=None, right=None):
        self.point = point
        self.split_dim = split_dim
        self.left = left
        self.right = right


def build_kdtree(points, depth=0):
    if not points:
        return None
    k = len(points[0])
    axis = depth % k
    sorted_points = sorted(points, key=lambda x: x[axis])
    mid = len(sorted_points) // 2
    # pointxy.append((sorted_points[mid][0],sorted_points[mid][1]*600))
    pointxy.append(sorted_points[mid])
    return Node(
        sorted_points[mid],
        axis,
        build_kdtree(sorted_points[:mid], depth + 1),
        build_kdtree(sorted_points[mid+1:], depth + 1)
    )

def display_node(node, canvas, x, y, w, h, cnt):

    if not node:
        return
    if node.left == None and node.right == None:
        return
    px = 50 + node.point[0] * 500
    py = 50 + node.point[1] * 500

    px = round(px, 2)
    py = round(py, 2)

    print("line printed ",px,py)
    if node.split_dim == 0:
        canvas.create_line(px, y, px, y+h)
        pointx = str(px)
        pointy = str(py)
        print(px, py, cnt, px, y, px, y+h, sep=",")

    else:
        canvas.create_line(x, py, x+w, py)
        pointx = str(px)
        pointy = str(py)
        print(px, py, cnt, x, py, x+w, py, sep=",")
    display_node(node.left, canvas, x, y, w if node.split_dim ==1 else px-x, h if node.split_dim == 0 else py-y, cnt+1)
    display_node(node.right, canvas, px if node.split_dim == 0 else x, py if node.split_dim ==1 else y, w if node.split_dim == 1 else x+w-px, h if node.split_dim == 0 else y+h-py, cnt+1)


def draw_points(points, canvas, x, y, w, h):
    for p in points:
        px = x + p[0] * w
        py = y + p[1] * h
        px = round(px, 2)
        py = round(py, 2)
        pointx = str(px)
        pointy = str(py)

        canvas.create_text(px, py+10, text="("+pointx+","+pointy+")")
        canvas.create_oval(px-2, py-2, px+2, py+2, fill="blue")

stop=1
def submit_action(val,val1,canvas):
    
    print(f"The input value is {val} {val1}")
    val = int(val)
    val1 = int(val1)
    
    points.append(((val-50)/500,(val1-50)/500))
    root = build_kdtree(points)
    
    canvas.create_rectangle(50, 50, 550, 550, fill='white', outline='white')
    
    draw_points(points, canvas, 50, 50, 500, 500)
    display_node(root, canvas, 50, 50, 500, 500, 0)
    print("this is new tree")
    draw_tree(root,canvas,1000,100,200,50)
    
    print(len(points))


    
def draw_tree(root, canvas, x, y, x_diff, y_diff):
    if root:
        px = 50 + root.point[0] * 500
        py = 50 + root.point[1] * 500

        px = round(px, 2)
        py = round(py, 2)
        print(root.point,root.split_dim,sep="  ")

        
        canvas.create_oval(x-25, y-25, x+25, y+25, fill="yellow")
        canvas.after(1000)
        canvas.update()
        canvas.create_text(x, y, text=str(px)+","+str(py))
        if root.left:
            canvas.create_line(x, y, x-x_diff, y+y_diff)
            draw_tree(root.left, canvas, x-x_diff, y+y_diff, x_diff/2, y_diff)
        if root.right:
            canvas.create_line(x, y, x+x_diff, y+y_diff)
            draw_tree(root.right, canvas, x+x_diff, y+y_diff, x_diff/2, y_diff)
        
    
def search_action(root,x,y,canvas):

    if root== None:
        return

    print(f'this is found {x} {y}')
    
    if root.point[0]==x and root.point[1]==y:
        print(f'this is found {x} {y}')
        return
    
    
    if root.point[0]>x:
        search_action(root.left,x,y,canvas)
    elif root.point[0]<x:
        search_action(root.right,x,y,canvas)
    elif root.point[0]==x:
        if root.point[1]>y:
            search_action(root.left,x,y,canvas)
        elif root.point[1]<y:
            search_action(root.right,x,y,canvas)
        if root.left.point[1]<y and root.right.point[1]>y and root.point[1]!=y :
            print("point not found") 
            return;


def draw_kdtree(root, points):
    root_window = tk.Tk()
    root_window.title("KD Tree")
    canvas_width = 1000
    canvas_height = 900
    canvas = tk.Canvas(root_window, width=canvas_width, height=canvas_height)
    canvas.config(scrollregion=(0,0,1500,900))
    
    yscrollbar = tk.Scrollbar(root_window, orient=tk.VERTICAL, command=canvas.yview)
    yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=yscrollbar.set)
    

    # Create a horizontal scrollbar at the bottom of the canvas
    xscrollbar = tk.Scrollbar(root_window, orient=tk.HORIZONTAL, command=canvas.xview)
    xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.configure(xscrollcommand=xscrollbar.set)
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH , expand= True)
    
    canvas.update_idletasks()
    canvas.configure(scrollregion = canvas.bbox('all'),xscrollincrement=1,yscrollincrement=1)
    yscrollbar.configure(command = canvas.yview)
    
    # canvas.update_idletasks()
    # canvas.configure(scrollregion=canvas.bbox('all'))
    xscrollbar.configure(command=canvas.xview)

    # create Entry widget
    entry = tk.Entry(canvas)
    canvas.create_window(100, 20, window=entry)
    
    entry1 = tk.Entry(canvas)
    canvas.create_window(100,50,window= entry1)

    # create Submit button
    submit_btn = tk.Button(canvas, text="Submit", command=lambda: submit_action(entry.get(),entry1.get(),canvas))
    canvas.create_window(200, 20, window=submit_btn)
    root_window.mainloop()


points = []
points.clear()
print(points)
print(len(points))

# build the kd tree
root = build_kdtree(points)
draw_kdtree(root, points)