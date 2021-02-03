from main import Main
import asyncio


if __name__ == "__main__":
    asyncio.Task(Main().task_check_email())
    asyncio.Task(Main().task_check_phone())
    Main()._run()