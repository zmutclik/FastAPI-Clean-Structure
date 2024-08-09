import time
import json

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

    def parse_params(self, request: Request):
        path_params = {}
        for route in request.app.router.routes:
            match, scope = route.matches(request)
            if match == Match.FULL:
                for name, value in scope["path_params"].items():
                    path_params[name] = value
        return json.dumps(path_params)

    async def start(self, request: Request):
        request.state.username = None
        user_agent = parse(request.headers.get("user-agent"))
        self.data = dataLogs(
            startTime=self.startTime,
            app=APP_NAME,
            platform=user_agent.os.family + user_agent.os.version_string,
            browser=user_agent.browser.family + user_agent.browser.version_string,
            path=request.scope["path"],
            path_params=self.parse_params(request),
            method=request.method,
            ipaddress=request.client.host,
        )
        return request

    async def finish(self, request: Request, response: Response):
        self.data.username = request.state.username
        self.data.status_code = response.status_code
        self.data.process_time = time.time() - self.startTime

        self.repository.create(self.data.model_dump())

        return self.data.process_time
