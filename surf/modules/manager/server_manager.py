# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/22 2:53
File Name       : server_manager
Last Edit Time  : 
"""
import asyncio
from typing import Dict, Optional

from surf.appsGlobal import get_logger
from surf.modules.manager import SurfUser

_con_log = get_logger('server_manager')


class SurfChannel(object):
    def __init__(self, channel_id: str, is_voice_channel: bool, max_members: int = 0):
        self.channel_id = channel_id
        self.is_voice_channel = is_voice_channel
        self.max_members = max_members
        self.channel_users: Dict[str, SurfUser] = {}
        self.lock = asyncio.Lock()

    async def add_user(self, user: SurfUser) -> bool:
        async with self.lock:
            if 0 < self.max_members <= len(self.channel_users):
                _con_log.warning(f"Channel {self.channel_id} is full. Max:{self.max_members}")
                return False
            self.channel_users[user.user_id] = user
            _con_log.info(f"User {user.nick_name} added to channel {self.channel_id}")
            return True

    async def remove_user(self, user_id: str) -> None:
        async with self.lock:
            if user_id in self.channel_users:
                del self.channel_users[user_id]
                _con_log.info(f"User {user_id} removed from channel {self.channel_id}")
            else:
                _con_log.error(f"Attempted to remove a none-existent user {user_id} from channel {self.channel_id}")

    async def broadcast(self, message: str) -> None:
        async with self.lock:
            users = list(self.channel_users.values())
        broadcast_tasks = [user.consumer.send(message) for user in users]
        await asyncio.gather(*broadcast_tasks, return_exceptions=True)
        _con_log.info(f'Broadcast message to channel {self.channel_id}')


class SurfServer(object):
    def __init__(self, server_id: str):
        self.server_id = server_id
        self.channels: Dict[str, SurfChannel] = {}
        self.lock = asyncio.Lock()

    async def add_channel(self, channel: SurfChannel) -> None:
        async with self.lock:
            if channel.channel_id in self.channels:
                _con_log.warning(f"Channel {channel.channel_id} already exist in server {self.server_id}")
                return
            self.channels[channel.channel_id] = channel
            _con_log.info(f'Channel {channel.channel_id} added to server {self.server_id}.')

    async def remove_channel(self, channel_id: str) -> None:
        async with self.lock:
            if channel_id in self.channels:
                del self.channels[channel_id]
                _con_log.info(f'Channel {channel_id} removed from server {self.server_id}')
            else:
                _con_log.error(f'Attempted to remove non-existent channel {channel_id} from server {self.server_id}.')

    async def get_channel(self, channel_id: str) -> Optional[SurfChannel]:
        async with self.lock:
            return self.channels.get(channel_id, None)

    async def get_all_channels(self) -> Dict[str, SurfChannel]:
        async with self.lock:
            return dict(self.channels)


class ServerManager(object):
    def __init__(self):
        self._servers: Dict[str, SurfServer] = {}
        self._lock = asyncio.Lock()
        _con_log.info(f"Initializing SurfManager")

    async def add_server(self, server_id: str) -> SurfServer:
        """
        :TODO 待定修改如果服务器已存在的问题
        :param server_id:
        :return:
        """
        async with self._lock:
            if server_id in self._servers:
                _con_log.warning(f"Server {server_id} already exists in manager")
            new_server = SurfServer(server_id)
            self._servers[server_id] = new_server
            _con_log.info(f"Server {server_id} added to manager")
            return new_server

    async def remove_server(self, server_id: str) -> None:
        async with self._lock:
            if server_id in self._servers:
                del self._servers[server_id]
                _con_log.info(f"Server {server_id} removed from manager")
            else:
                _con_log.error(f"Attempted to remove non-existent server {server_id} from manager")

    async def get_server(self, server_id: str) -> Optional[SurfServer]:
        async with self._lock:
            return self._servers.get(server_id, None)

    async def get_all_servers(self) -> Dict[str, SurfServer]:
        async with self._lock:
            return dict(self._servers)
