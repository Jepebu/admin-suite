import tkinter as tk

class Tile(tk.Label):
    def __init__(self, parent, text):
        tk.Label.__init__(self, parent, text=text, relief=tk.RAISED, bd=1)
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.dragging = False
        self.start_index = 0
    
    def on_button_press(self, event):
        self.start_index = self.master.master.tiles.index(self)
        self.dragging = True
        self._drag_data = {'x': event.x, 'y': event.y}
        self.place(x=self.winfo_x(), y=self.winfo_y())
        print(f"Tile {self.start_index} clicked")
    
    def on_move(self, event):
        if self.dragging:
            delta_x = event.x - self._drag_data['x']
            delta_y = event.y - self._drag_data['y']
            self.place(x=self.winfo_x() + delta_x, y=self.winfo_y() + delta_y)
            self.check_for_swap()
    
    def on_button_release(self, event):
        if self.dragging:
            self.dragging = False
            self.place(x=self.winfo_x(), y=self.winfo_y())
            self.check_for_swap()
    
    def check_for_swap(self):
        for tile in self.master.master.tiles:
            if tile != self and self.intersects(tile):
                target_index = self.master.master.tiles.index(tile)
                print(f"Swapping tile {self.start_index} with tile {target_index}")
                self.master.master.tiles[self.start_index], self.master.master.tiles[target_index] = self.master.master.tiles[target_index], self.master.master.tiles[self.start_index]
                self.master.redraw_tiles()
                break
    
    def intersects(self, tile):
        x1, y1, x2, y2 = self.master.master.bbox(tile)
        return (x1 <= self.winfo_x() <= x2 and y1 <= self.winfo_y() <= y2) or \
               (x1 <= self.winfo_x() + self.winfo_width() <= x2 and y1 <= self.winfo_y() <= y2) or \
               (x1 <= self.winfo_x() <= x2 and y1 <= self.winfo_y() + self.winfo_height() <= y2) or \
               (x1 <= self.winfo_x() + self.winfo_width() <= x2 and y1 <= self.winfo_y() + self.winfo_height() <= y2)


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.tiles = []
        
        self.title("Drag and Swap Tiles")
        self.geometry("600x400")
        
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack()
        
        self.create_tiles()
    
    def create_tiles(self):
        tile_texts = ['Tile 1', 'Tile 2', 'Tile 3', 'Tile 4', 'Tile 5']
        tile_count = len(tile_texts)
        
        tile_width = self.canvas.winfo_width() // tile_count
        tile_height = self.canvas.winfo_height() // tile_count
        
        for i, text in enumerate(tile_texts):
            tile = Tile(self.canvas, text)
            x = i * (self.canvas.winfo_width() - tile_width) // (tile_count - 1)
            y = i * (self.canvas.winfo_height() - tile_height) // (tile_count - 1)
            tile.place(x=x, y=y, width=tile_width, height=tile_height)
            tile.config(relief=tk.SOLID, borderwidth=1)
            tile.config(anchor=tk.CENTER)
            self.tiles.append(tile)
            self.canvas.create_window((x, y), window=tile, width=tile_width, height=tile_height)
        
        print("Tiles created successfully")
    
    def redraw_tiles(self):
        self.canvas.delete("all")
        self.create_tiles()
        print("Tiles redrawn successfully")

if __name__ == "__main__":
    app = Application()
    app.redraw_tiles()  # Call redraw_tiles() to initially display the tiles
    app.mainloop()

