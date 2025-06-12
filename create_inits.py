import os

#create __init__.py files in specified folders
folders = [
    "app",
    "app/api",
    "app/api/routes"
    "app/auth",
    "app/db",
    "app/schemas",
    "app/utils",
    "app/predict",
]
# Ensure the folders exist
for folder in folders:
    os.makedirs(folder, exist_ok=True)
for folder in folders:
    init_path = os.path.join(folder, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            pass  
        print(f"Created {init_path}")
    else:
        print(f"{init_path} already exists")