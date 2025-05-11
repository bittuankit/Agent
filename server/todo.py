from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("todo")

@mcp.tool()
async def get_task():
    with open("data/todo.json", "r") as file:
        file_data = json.load(file)
        return file_data    

@mcp.tool()
async def add_task(input: dict):
    with open("data/todo.json", "r+") as file:
        file_data = json.load(file)
        file_data["tasks"].append(input)
        file.seek(0)
        json.dump(file_data, file, indent = 2)
        return "Task added successfully"

@mcp.tool()
async def delete_task(input: dict):
    with open("data/todo.json", "r+") as file:
        file_data = json.load(file)
        for task in file_data["tasks"]:
            if task["id"] == input["id"]:
                file_data["tasks"].remove(task)
                break
        file.seek(0)
        json.dump(file_data, file, indent = 2)
        return "Task deleted successfully"  

@mcp.tool()
async def update_task(input: dict):
    with open("data/todo.json", "r+") as file:
        file_data = json.load(file) 
        for task in file_data["tasks"]:
            if task["id"] == input["id"]:
                task["task"] = input["task"]
                break
        file.seek(0)
        json.dump(file_data, file, indent = 2)
        return "Task updated successfully"  

