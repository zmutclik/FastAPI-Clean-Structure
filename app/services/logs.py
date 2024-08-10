import time
import json

import string
import random

from fastapi import Request, Response
from starlette.routing import Match
from user_agents import parse

from app.schemas.logs import dataLogs
from app.repositories.logs import LogsRepository
from app.core.env import APP_NAME


class LogServices:

    def __init__(self):
        self.repository = LogsRepository()
        self.startTime = time.time()
        clientId_key = APP_NAME.lower() + "_id"
        self.clientId_key = clientId_key.replace(" ", "_")

    def parse_params(self, request: Request):
        path_params = {}
        for route in request.app.router.routes:
            match, scope = route.matches(request)
            if match == Match.FULL:
                for name, value in scope["path_params"].items():
                    path_params[name] = value
        return json.dumps(path_params)

    def clientId(self, request: Request):
        clientId = request.cookies.get(self.clientId_key)
        if clientId is None:
            self.clientId_new = True
            return "".join(random.choices(string.ascii_letters + string.digits, k=32))
        self.clientId_new = False
        return clientId

    async def start(self, request: Request):
        request.state.username = None
        user_agent = parse(request.headers.get("user-agent"))
        self.data = dataLogs(
            startTime=self.startTime,
            app=APP_NAME,
            client_id=self.clientId(request),
            platform=user_agent.os.family + user_agent.os.version_string,
            browser=user_agent.browser.family + user_agent.browser.version_string,
            path=request.scope["path"],
            path_params=self.parse_params(request),
            method=request.method,
            ipaddress=request.client.host,
        )
        request.state.client_id = self.data.client_id
        return request

    async def finish(self, request: Request, response: Response):
        self.data.username = request.state.username
        self.data.status_code = response.status_code
        self.data.process_time = time.time() - self.startTime
        if self.clientId_new:
            response.set_cookie(key=self.clientId_key, value=self.data.client_id)

        self.repository.create(self.data.model_dump())
