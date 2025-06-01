import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
from collections import deque
from PIL import Image, ImageTk

class Guard:
    def __init__(self, name, start_room):
        self.name = name
        self.current_room = start_room
        self.status = "Idle"
        self.icon = None
        self.icon_text = None
        self.color = random.choice(['#FF9800', '#8E44AD', '#27AE60', '#E91E63', '#00BCD4'])
        self.patrol_speed = random.uniform(0.5, 1.5)
        self.patrolling = False
        self.alarm_room = None
        self.patrol_path = []
        self.current_path_index = 0
        self.patrol_type = "DFS"  # Default patrol type
        self.is_chief = False

    def update_status(self, new_status):
        self.status = new_status

class MuseumMap:
    def __init__(self):
        self.rooms = {
            "Main Hall": ["Antiquity Hall", "Painting Gallery", "Sculpture Wing", "Ticket Booth"],
            "Antiquity Hall": ["Main Hall", "Secure Storage", "Egyptian Gallery"],
            "Painting Gallery": ["Main Hall", "Modern Art Room"],
            "Sculpture Wing": ["Main Hall", "Renaissance Hall"],
            "Ticket Booth": ["Main Hall", "Gift Shop"],
            "Gift Shop": ["Ticket Booth", "Cafeteria"],
            "Cafeteria": ["Gift Shop", "Staff Lounge"],
            "Staff Lounge": ["Cafeteria", "Security Office"],
            "Security Office": ["Staff Lounge", "Control Room"],
            "Control Room": ["Security Office"],
            "Egyptian Gallery": ["Antiquity Hall", "Greek Gallery"],
            "Greek Gallery": ["Egyptian Gallery", "Roman Gallery"],
            "Roman Gallery": ["Greek Gallery"],
            "Modern Art Room": ["Painting Gallery", "Contemporary Wing"],
            "Contemporary Wing": ["Modern Art Room"],
            "Renaissance Hall": ["Sculpture Wing", "Baroque Room"],
            "Baroque Room": ["Renaissance Hall"],
            "Manuscript Room": ["East Entrance", "Secure Storage"],
            "Secure Storage": ["Antiquity Hall", "Manuscript Room", "Vault"],
            "Vault": ["Secure Storage"],
            "East Entrance": ["Manuscript Room"]
        }
        
        # Room importance levels (for patrol prioritization)
        self.room_importance = {
            "Vault": 5,
            "Secure Storage": 4,
            "Control Room": 4,
            "Security Office": 3,
            "Main Hall": 3,
            "Antiquity Hall": 2,
            "Painting Gallery": 2,
            "Sculpture Wing": 2,
            "Ticket Booth": 1,
            "Gift Shop": 1,
            "Cafeteria": 1,
            "Staff Lounge": 2,
            "Egyptian Gallery": 2,
            "Greek Gallery": 2,
            "Roman Gallery": 2,
            "Modern Art Room": 2,
            "Contemporary Wing": 1,
            "Renaissance Hall": 2,
            "Baroque Room": 1,
            "Manuscript Room": 2,
            "East Entrance": 2
        }

    def get_neighbors(self, room):
        return self.rooms.get(room, [])

    def dfs_path(self, start):
        visited = set()
        path = []

        def dfs(room):
            if room in visited:
                return
            visited.add(room)
            path.append(room)
            # Sort neighbors by importance (higher importance first)
            neighbors = sorted(self.get_neighbors(room), 
                             key=lambda x: self.room_importance[x], 
                             reverse=True)
            for neighbor in neighbors:
                dfs(neighbor)

        dfs(start)
        return path

    def bfs_path(self, start):
        visited = set()
        queue = deque([start])
        path = []
        
        while queue:
            room = queue.popleft()
            if room not in visited:
                visited.add(room)
                path.append(room)
                # Sort neighbors by importance (higher importance first)
                neighbors = sorted(self.get_neighbors(room), 
                                 key=lambda x: self.room_importance[x], 
                                 reverse=True)
                queue.extend(neighbors)
        return path

    def random_path(self, start, length=20):
        path = [start]
        current = start
        for _ in range(length):
            neighbors = self.get_neighbors(current)
            if not neighbors:
                break
            current = random.choice(neighbors)
            path.append(current)
        return path

    def bfs_path_to_target(self, start, target):
        visited = set()
        queue = deque([[start]])
        while queue:
            path = queue.popleft()
            room = path[-1]
            if room == target:
                return path
            if room not in visited:
                visited.add(room)
                for neighbor in sorted(self.get_neighbors(room)):
                    queue.append(path + [neighbor])
        return []

class MuseumGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Museum Guard Patrol Simulation")
        self.root.geometry("1200x800")

        self.map = MuseumMap()
        self.guards = []
        self.alarm_active = False
        self.alarm_room = None
        self.chief_guard = None

        self.rooms_pos = {
            "Main Hall": (400, 300),
            "Antiquity Hall": (550, 300),
            "Painting Gallery": (400, 150),
            "Sculpture Wing": (400, 450),
            "Ticket Booth": (250, 300),
            "Gift Shop": (200, 200),
            "Cafeteria": (150, 100),
            "Staff Lounge": (100, 50),
            "Security Office": (100, 150),
            "Control Room": (100, 250),
            "Egyptian Gallery": (700, 300),
            "Greek Gallery": (850, 300),
            "Roman Gallery": (1000, 300),
            "Modern Art Room": (400, 50),
            "Contemporary Wing": (400, 0),
            "Renaissance Hall": (550, 450),
            "Baroque Room": (700, 450),
            "Manuscript Room": (850, 150),
            "Secure Storage": (700, 150),
            "Vault": (700, 50),
            "East Entrance": (1000, 150)
        }

        self.create_widgets()
        self.add_guard("Guard 1", "Main Hall")
        self.draw_map()
        self.start_alarm_simulation()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg='white', width=900, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(self.main_frame, width=300)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(control_frame, text="Guard Controls", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Add Chief Security button
        ttk.Button(control_frame, text="Add Chief Security", 
                   command=lambda: self.add_guard("Chief Security", "Security Office", is_chief=True)).pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="Add Guard", command=self.add_guard_ui).pack(fill=tk.X, pady=5)

        self.guard_listbox = tk.Listbox(control_frame)
        self.guard_listbox.pack(fill=tk.X)

        # Patrol options
        ttk.Label(control_frame, text="Patrol Options", font=('Arial', 10, 'bold')).pack(pady=5)
        self.patrol_type = tk.StringVar(value="DFS")
        ttk.Radiobutton(control_frame, text="DFS Patrol", variable=self.patrol_type, value="DFS").pack(anchor=tk.W)
        ttk.Radiobutton(control_frame, text="BFS Patrol", variable=self.patrol_type, value="BFS").pack(anchor=tk.W)
        ttk.Radiobutton(control_frame, text="Random Patrol", variable=self.patrol_type, value="Random").pack(anchor=tk.W)

        ttk.Button(control_frame, text="Start Patrol", command=self.start_patrol).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="Stop Patrol", command=self.stop_patrol).pack(fill=tk.X, pady=5)

        ttk.Label(control_frame, text="Alarm", font=('Arial', 12, 'bold')).pack(pady=10)
        self.alarm_room_var = tk.StringVar()
        self.alarm_room_combo = ttk.Combobox(control_frame, textvariable=self.alarm_room_var, 
                                           values=list(self.rooms_pos.keys()))
        self.alarm_room_combo.pack(fill=tk.X)
        self.alarm_room_combo.current(0)

        ttk.Button(control_frame, text="Trigger Alarm", command=self.trigger_alarm).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="Clear Alarm", command=self.clear_alarm).pack(fill=tk.X, pady=5)

        ttk.Label(control_frame, text="Event Log", font=('Arial', 12, 'bold')).pack(pady=10)
        self.log_text = tk.Text(control_frame, height=10, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def draw_map(self):
        self.canvas.delete("all")
        # Draw connections
        for room, neighbors in self.map.rooms.items():
            x1, y1 = self.rooms_pos[room]
            for neighbor in neighbors:
                x2, y2 = self.rooms_pos[neighbor]
                self.canvas.create_line(x1, y1, x2, y2, fill='gray')

        # Draw rooms
        for room, pos in self.rooms_pos.items():
            x, y = pos
            fill = 'red' if self.alarm_active and room == self.alarm_room else 'lightblue'
            outline = 'black'
            width = 1
            
            # Highlight important rooms
            if self.map.room_importance[room] >= 4:
                outline = 'red'
                width = 3
            elif self.map.room_importance[room] >= 3:
                outline = 'orange'
                width = 2
            
            self.canvas.create_rectangle(x-30, y-30, x+30, y+30, 
                                       fill=fill, outline=outline, width=width)
            self.canvas.create_text(x, y, text=room, font=('Arial', 8))

        # Draw guards
        for guard in self.guards:
            x, y = self.rooms_pos[guard.current_room]
            # Offset position if multiple guards in same room
            idx = self.guards.index(guard)
            offset_x = (idx % 3) * 10 - 10
            offset_y = (idx // 3) * 10 - 10
            
            # Chief gets a star icon
            if guard.is_chief:
                guard.icon = self.canvas.create_polygon(
                    x+offset_x-15, y+offset_y+5,
                    x+offset_x-5, y+offset_y+5,
                    x+offset_x, y+offset_y-5,
                    x+offset_x+5, y+offset_y+5,
                    x+offset_x+15, y+offset_y+5,
                    x+offset_x+5, y+offset_y+10,
                    x+offset_x+10, y+offset_y+20,
                    x+offset_x, y+offset_y+15,
                    x+offset_x-10, y+offset_y+20,
                    x+offset_x-5, y+offset_y+10,
                    fill=guard.color, outline='black'
                )
            else:
                guard.icon = self.canvas.create_oval(
                    x+offset_x-15, y+offset_y-15, 
                    x+offset_x+15, y+offset_y+15, 
                    fill=guard.color)
            
            guard.icon_text = self.canvas.create_text(
                x+offset_x, y+offset_y, 
                text=guard.name[0], 
                fill='white',
                font=('Arial', 10, 'bold'))
            
            # Draw status text
            self.canvas.create_text(
                x+offset_x, y+offset_y+25, 
                text=guard.status, 
                font=('Arial', 8))

    def add_guard(self, name, start_room, is_chief=False):
        guard = Guard(name, start_room)
        guard.is_chief = is_chief
        if is_chief:
            guard.color = '#FF0000'  # Chief gets red color
            guard.patrol_speed = 0.8  # Chief moves faster
            self.chief_guard = guard
        self.guards.append(guard)
        self.guard_listbox.insert(tk.END, name)
        self.log_event(f"{name} added at {start_room}")
        self.draw_map()

    def add_guard_ui(self):
        name = f"Guard {len(self.guards)+1}"
        self.add_guard(name, "Main Hall")

    def start_patrol(self):
        if not self.guards:
            return

        selected = self.guard_listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Guard", "Please select a guard to patrol.")
            return

        guard = self.guards[selected[0]]
        patrol_type = self.patrol_type.get()
        guard.patrol_type = patrol_type
        
        if patrol_type == "DFS":
            guard.patrol_path = self.map.dfs_path(guard.current_room)
        elif patrol_type == "BFS":
            guard.patrol_path = self.map.bfs_path(guard.current_room)
        else:  # Random
            guard.patrol_path = self.map.random_path(guard.current_room)
        
        guard.patrolling = True
        guard.current_path_index = 0
        guard.update_status(f"Patrolling ({patrol_type})")
        self.log_event(f"{guard.name} started {patrol_type} patrol")

        def patrol():
            while guard.patrolling and not self.alarm_active:
                if guard.current_path_index >= len(guard.patrol_path):
                    # Reached end of path, generate new one based on patrol type
                    if patrol_type == "DFS":
                        guard.patrol_path = self.map.dfs_path(guard.current_room)
                    elif patrol_type == "BFS":
                        guard.patrol_path = self.map.bfs_path(guard.current_room)
                    else:  # Random
                        guard.patrol_path = self.map.random_path(guard.current_room)
                    guard.current_path_index = 0
                
                guard.current_room = guard.patrol_path[guard.current_path_index]
                guard.current_path_index += 1
                self.root.after(0, self.draw_map)
                time.sleep(guard.patrol_speed)

            if self.alarm_active and guard.patrolling:
                # Chief responds faster and more efficiently
                response_speed = 0.3 if guard.is_chief else 0.5
                guard.update_status("Responding to Alarm")
                path = self.map.bfs_path_to_target(guard.current_room, self.alarm_room)
                if path:
                    for room in path[1:]:
                        if not guard.patrolling or not self.alarm_active:
                            break
                        guard.current_room = room
                        self.root.after(0, self.draw_map)
                        time.sleep(guard.patrol_speed * response_speed)
                guard.update_status("Idle")

            guard.patrolling = False
            self.root.after(0, self.draw_map)

        threading.Thread(target=patrol, daemon=True).start()

    def stop_patrol(self):
        selected = self.guard_listbox.curselection()
        if not selected:
            return
        guard = self.guards[selected[0]]
        guard.patrolling = False
        guard.update_status("Idle")
        self.log_event(f"{guard.name} patrol stopped")
        self.draw_map()

    def trigger_alarm(self):
        self.alarm_room = self.alarm_room_var.get()
        self.alarm_active = True
        self.log_event(f"ALARM TRIGGERED in {self.alarm_room}")
        
        # Notify all guards
        for guard in self.guards:
            if guard.patrolling:
                guard.update_status("Responding to Alarm")
        
        # If chief is available, have them respond first
        if self.chief_guard and not self.chief_guard.patrolling:
            self.guard_listbox.selection_clear(0, tk.END)
            self.guard_listbox.selection_set(self.guards.index(self.chief_guard))
            self.start_patrol()
        
        self.draw_map()

    def clear_alarm(self):
        self.alarm_active = False
        self.alarm_room = None
        self.log_event("Alarm cleared")
        self.draw_map()

    def start_alarm_simulation(self):
        def simulate():
            while True:
                if random.random() < 0.1 and not self.alarm_active:
                    # Higher probability for important rooms
                    rooms = list(self.rooms_pos.keys())
                    weights = [self.map.room_importance[room] for room in rooms]
                    alarm_room = random.choices(rooms, weights=weights, k=1)[0]
                    self.root.after(0, lambda: self.trigger_alarm_in_room(alarm_room))
                time.sleep(10)

        threading.Thread(target=simulate, daemon=True).start()

    def trigger_alarm_in_room(self, room):
        self.alarm_room_var.set(room)
        self.trigger_alarm()

    def log_event(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Load and display the image
    try:
        img = Image.open("image.png")
        img = img.resize((300, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=photo)
        label.image = photo
        label.pack()
    except:
        print("Image not found or couldn't be loaded")
    
    app = MuseumGUI(root)
    root.mainloop()