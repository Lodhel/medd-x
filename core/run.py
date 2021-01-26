from main import Main
import asyncio


if __name__ == "__main__":
    asyncio.Task(Main().task_check_email())
    Main()._run()