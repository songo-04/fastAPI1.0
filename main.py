from fastapi import FastAPI 
from routes.entry_point import entry_root
from routes.user_route import user_root
from routes.contact_route import contact_route
from routes.task_route import task_route

app= FastAPI()

app.include_router(entry_root)
app.include_router(user_root)
app.include_router(contact_route)
app.include_router(task_route)