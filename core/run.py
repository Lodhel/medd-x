from main import Main
import asyncio


if __name__ == "__main__":
    asyncio.Task(Main().task_check_email())
    asyncio.Task(Main().task_check_phone())
    asyncio.Task(Main().task_is_active())
    asyncio.Task(Main().task_is_step())
    asyncio.Task(Main().task_let_sms())
    asyncio.Task(Main().task_let_email())
    Main()._run()