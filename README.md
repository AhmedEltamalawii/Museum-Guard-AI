** 🏛️ Museum Guard Patrol Simulation 🚨 **

Welcome to the Museum Guard Patrol Simulation! This project brings to life the intricate dance of security within a bustling museum. Watch as vigilant guards navigate the halls, employing different strategies to keep precious artifacts safe, and see how they react when an alarm shatters the tranquility.

## ✨ Features

*   **Dynamic Museum Map:** Explore a detailed map of the museum, complete with various halls, galleries, and critical security areas like the Vault and Control Room.
*   **Guard Management:** Deploy multiple guards, each with their own unique color and patrol speed. Introduce the Chief Security Guard, who boasts enhanced speed and response capabilities!
*   **Intelligent Patrol Algorithms:** Assign guards different patrol strategies:
    *   **DFS (Depth-First Search):** Guards delve deep into connected areas, prioritizing important rooms.
    *   **BFS (Breadth-First Search):** Guards explore layer by layer, also considering room importance.
    *   **Random Patrol:** For unpredictable movements, guards wander through adjacent rooms.
*   **Real-time Alarm System:** Simulate security breaches by triggering alarms in any room. Watch the map change visually and observe how guards alter their routes.
*   **Prioritized Response:** Guards, especially the Chief, will drop their regular patrols and swiftly navigate to the alarm location using an efficient pathfinding algorithm (BFS).
*   **Visual Simulation:** A clean and intuitive Graphical User Interface (GUI) built with Tkinter visualizes the museum layout, guard positions, statuses, and alarm locations in real-time.
*   **Room Importance Hierarchy:** Rooms are assigned importance levels, influencing patrol path generation and the probability of random alarms occurring in critical areas.
*   **Event Logging:** A built-in log tracks key events, providing a clear history of guard activities and alarm incidents.

## 🛠️ Technologies Used

*   **Python:** The core programming language powering the simulation logic.
*   **Tkinter:** Python's standard GUI library, used to create the interactive and visual interface.
*   **Threading:** Allows the simulation logic (guard patrols, alarm simulation) to run concurrently with the GUI, ensuring a smooth experience.
*   **Pillow (PIL Fork):** Used for loading and displaying images within the GUI (specifically `image.png`).
*   **Collections (deque):** Utilized in the BFS algorithm for efficient pathfinding.
*   **Random:** Adds elements of unpredictability to guard movements and alarm occurrences.

## ▶️ How to Run

1.  **Prerequisites:** Make sure you have Python installed.
2.  **Install Dependencies:** This project requires the Pillow library. You can install it using pip:
    ```bash
    pip install Pillow
    ```
3.  **Save the Code:** Save the provided Python code as `last.py`.
4.  **(Optional) Add an Image:** If you have an image file named `image.png` in the same directory as `last.py`, the GUI will attempt to display it at the top.
5.  **Run the Script:** Open your terminal or command prompt, navigate to the directory where you saved `last.py`, and run:
    ```bash
    python last.py
    ```
6.  **Interact:** Use the controls in the GUI to add guards, select patrol types, start/stop patrols, and trigger/clear alarms. Observe the guards moving on the map and check the event log for updates!

Dive into the world of museum security and see if your guards can keep the treasures safe!
**
