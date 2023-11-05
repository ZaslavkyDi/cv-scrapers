import asyncio

from app.workua.process_executor import WorkUAExecutor


async def main() -> None:
    work_ua_runner = WorkUAExecutor()
    await work_ua_runner.run(position="адміністратор")

if __name__ == '__main__':
    asyncio.run(main())
