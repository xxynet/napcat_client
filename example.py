import asyncio
import logging

from napcat_client import NapCatWebSocketClient
from napcat_client import QQMessageChain, QQMessageType

logger = logging.getLogger(__name__)


async def main():
    client = NapCatWebSocketClient()

    @client.group_event()
    async def on_group_message(msg: dict):
        logger.info(f"收到群聊消息：{msg}")

    @client.private_event()
    async def on_private_message(msg: dict):
        logger.info(f"收到私聊消息：{msg}")
        msg_list = [QQMessageType.Text("收到私聊消息")]
        message_chain = QQMessageChain(msg_list)
        await client.send_direct_message(msg.get("user_id"), message_chain)

    @client.notice_event()
    async def on_notice_message(msg: dict):
        logger.info(f"收到通知消息：{msg}")

    @client.meta_event()
    async def on_meta_message(msg: dict):
        logger.info(f"收到元消息：{msg}")
        if msg.get("meta_event_type") == "lifecycle":
            client.login_success = True
            logger.info("登录成功")

    @client.napcat_event()
    async def on_napcat_message(msg: dict):
        if msg.get("status", "") == "failed":
            if msg.get("retcode") == 1403:
                logger.error("invalid token")
                await client.close()

    config = {
        "bot_pid": 123456789,
        "ws_uri": "ws://localhost:3001",
        "ws_token": "napcat"
    }

    await client.run(bt_uin=config["bot_pid"], ws_uri=config["ws_uri"], ws_token=config["ws_token"])


asyncio.run(main())
