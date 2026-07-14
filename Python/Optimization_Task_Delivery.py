import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 1. Parameters ---
N_ROBOTS = 7
TASKS_PER_ROBOT = 2
TIME_STEPS = 3500   
DELTA_T = 0.2
V_MAX = 6.0        
R_MAX = 24.0       
D_SAFE = 2.5
DELIVERY_RADIUS = 1.2
JITTER_BASE = 2.0  

COLORS = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#F3FF33', '#33FFFF', '#FF8333']

np.random.seed(21)
curr_pos = np.random.uniform(45, 55, (N_ROBOTS, 2))

# --- Fixed Task Table Creation ---
task_list = []
for i in range(N_ROBOTS):
    for _ in range(TASKS_PER_ROBOT):
        target = np.random.uniform(5, 95, 2)
        priority = np.random.uniform(5, 15)
        # Store individual coordinates separately to keep the array homogeneous
        task_list.append([target[0], target[1], priority, 1.0, float(i)])
tasks = np.array(task_list)

# --- 2. Swarm Engine ---
history = [curr_pos.copy()]
task_status_history = [tasks[:, 3].copy()]

print("Simulation started. Breaking North/South symmetry via Leader Election...")

for t in range(TIME_STEPS):
    new_pos = curr_pos.copy()
    
    # --- GLOBAL LEADER ELECTION ---
    # Find all active tasks and identify the one with the single highest priority
    active_task_info = [] # List of (priority, robot_id)
    for r_id in range(N_ROBOTS):
        my_active = np.where((tasks[:, 4] == r_id) & (tasks[:, 3] == 1.0))[0]
        if len(my_active) > 0:
            # Look at the priority of the NEXT task in this robot's sequence
            prio = tasks[my_active[0], 2]
            active_task_info.append((prio, r_id))
    
    # Determine the Global Leader (Robot with the most urgent task)
    if active_task_info:
        # Sort by priority and pick the top one
        active_task_info.sort(key=lambda x: x[0], reverse=True)
        global_leader_id = active_task_info[0][1]
        active_robot_ids = [info[1] for info in active_task_info]
    else:
        global_leader_id = -1
        active_robot_ids = []

    # Calculate support centroid
    if active_robot_ids:
        active_centroid = np.mean([curr_pos[rid] for rid in active_robot_ids], axis=0)
    else:
        active_centroid = np.mean(curr_pos, axis=0)

    for i in range(N_ROBOTS):
        force = np.array([0.0, 0.0])
        
        # A. Task Pull Logic
        my_active = np.where((tasks[:, 4] == i) & (tasks[:, 3] == 1.0))[0]
        if len(my_active) > 0:
            idx = my_active[0]
            target_pos = tasks[idx, :2]
            direction = target_pos - curr_pos[i]
            dist = np.linalg.norm(direction)
            
            if dist > 0:
                pull_power = tasks[idx, 2] / 2.0
                
                # --- SYMMETRY BREAKER ---
                if i == global_leader_id:
                    pull_power *= 10.0  # Massive boost to leader
                else:
                    pull_power *= 0.4   # Others yield to prevent deadlocks
                
                if dist < 12.0:
                    pull_power *= (12.0 / (dist + 0.5))
                
                force += (direction / dist) * pull_power
            
            if dist < DELIVERY_RADIUS:
                tasks[idx, 3] = 0.0
        else:
            # SUPPORT ROLE
            support_dir = active_centroid - curr_pos[i]
            s_dist = np.linalg.norm(support_dir)
            if s_dist > 3.0:
                force += (support_dir / (s_dist + 1e-5)) * 3.0

        # B. Connectivity Force (Min 3 Neighbors)
        dists = []
        for j in range(N_ROBOTS):
            if i != j:
                dists.append((np.linalg.norm(curr_pos[i] - curr_pos[j]), j))
        dists.sort()
        
        third_dist = dists[2][0]
        if third_dist > R_MAX:
            # Leader can stretch more; followers stay tight
            leash_strength = 4.0 if i == global_leader_id else 10.0
            for k in range(3):
                n_idx = dists[k][1]
                pull_dir = curr_pos[n_idx] - curr_pos[i]
                force += (pull_dir / (dists[k][0] + 1e-5)) * leash_strength

        # C. Collision Avoidance
        for j in range(N_ROBOTS):
            if i != j:
                dist_ij = np.linalg.norm(curr_pos[i] - curr_pos[j])
                if dist_ij < D_SAFE:
                    force += ((curr_pos[i] - curr_pos[j]) / (dist_ij + 1e-5)) * 12.0

        # D. Jitter
        force += np.random.uniform(-1, 1, 2) * JITTER_BASE

        mag = np.linalg.norm(force)
        if mag > V_MAX: force = (force / mag) * V_MAX
        new_pos[i] += force * DELTA_T

    curr_pos = new_pos.copy()
    history.append(curr_pos.copy())
    task_status_history.append(tasks[:, 3].copy())

# --- 3. Visualization ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-5, 105); ax.set_ylim(-5, 105)
ax.set_title("Global Leader Election Swarm (Symmetry Resolved)")

robot_plots = [ax.plot([], [], 'o', color=COLORS[i], markersize=10, zorder=5)[0] for i in range(N_ROBOTS)]
task_plots = [ax.plot(tasks[i, 0], tasks[i, 1], 'X', color=COLORS[int(tasks[i, 4])], markersize=8, zorder=2)[0] for i in range(len(tasks))]
line_objs = [ax.plot([], [], 'g-', alpha=0.3, lw=1, zorder=1)[0] for _ in range(N_ROBOTS * (N_ROBOTS-1) // 2)]

def update(frame):
    pos, t_status = history[frame], task_status_history[frame]
    for i in range(N_ROBOTS): robot_plots[i].set_data([pos[i, 0]], [pos[i, 1]])
    for i in range(len(tasks)):
        task_plots[i].set_alpha(1.0 if t_status[i] == 1.0 else 0.1)
        if t_status[i] == 0.0: task_plots[i].set_marker('o')
    l_idx = 0
    for i in range(N_ROBOTS):
        for j in range(i + 1, N_ROBOTS):
            if np.linalg.norm(pos[i] - pos[j]) <= R_MAX:
                line_objs[l_idx].set_data([pos[i, 0], pos[j, 0]], [pos[i, 1], pos[j, 1]])
            else:
                line_objs[l_idx].set_data([], [])
            l_idx += 1
    return robot_plots + task_plots + line_objs

ani = FuncAnimation(fig, update, frames=len(history), interval=15, blit=True, repeat=False)
plt.grid(True, alpha=0.2); plt.show()
