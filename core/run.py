from main import Main
import asyncio


if __name__ == "__main__":
    asyncio.Task(Main().task_check_email())
    asyncio.Task(Main().task_check_phone())
    asyncio.Task(Main().task_is_active())
    asyncio.Task(Main().task_is_step())
    Main()._run()