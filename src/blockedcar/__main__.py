import asyncio

import logging

from aiogram import Bot, Dispatcher

from blockedcar.main.di.setup import setup_dishka

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> None:
    dishka = setup_dishka()

    bot = await dishka.get(Bot)
    dispatcher = await dishka.get(Dispatcher)

    try:
        logger.info("Bot starting. . .")
        await dispatcher.start_polling(bot)
    finally:
        await dishka.close()
        logger.info("Bot stopping. . .")


if __name__ == "__main__":
    asyncio.run(main())
