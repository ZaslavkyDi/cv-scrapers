import asyncio

from app.scrapers.workua.executor import WorkUAExecutor
from app.scrapers.robotaua import RobotaUAExecutor


async def workau_main() -> None:
    runner = WorkUAExecutor()
    await runner.run(position="адміністратор")


async def robotaua_main() -> None:
    runner = RobotaUAExecutor()
    await runner.run(position="Менеджер")


if __name__ == '__main__':
    asyncio.run(robotaua_main())
