import json

tasks = []

def add_tasks(task):
    tasks.append(task)
    print (f"Added:{task}")

add_tasks("go swimming")
add_tasks("code")

def show_tasks():
    if not tasks:
        print("no tasks yet")
        return
    
    print("/nYour tasks:")
    for i, task in enumerate(tasks):
        print(f"{i}.{task}")

show_tasks()

def update_task(index, new_task):
    if index < 0 or index >= len(tasks):
        print("invalid task number")
        return
    
    old = tasks[index]
    tasks[index] = new_task
    print(f"Updated: {old} -> {new_task}")

update_task(1, "go to the gym")
show_tasks()  

def delete_task(index):
    if index < 0 or index >= len(tasks):
        print("Invalid task number.")
        return

    removed = tasks.pop(index) 
    print(f"Deleted: {removed}")

delete_task(0)    
show_tasks()

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)
    print("tasks saved.") 

def load_tasks():
    global tasks
    try:
        with open("tasks.json","r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []          

load_tasks()
