from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
import time
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware



class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        # TODO:(Member) Finish implementing this method

        start_time = time.time()

        # get request details
        method = request.method
        url = str(request.url)
        if request.client:
            client = request.client.host
        else:
            client = "Unknown"

        logger.info(f"Incoming Request | Method: {method} | URL: {url} | Client: {client}")

        try:
            response = await call_next(request)

            process_time = (time.time() - start_time) * 1000  # in ms

            logger.info(
                f"Outgoing Response | Status: {response.status_code} | "
                f"Processing Time: {process_time:.3f}ms | "
                f"Method: {method} | URL: {url}"
            )
            
            return response

        except Exception as e:
            logger.error(
                f"Error Processing Request: {method} | URL: {url} | Client: {client}"
                f"Error: {e}"
            )
            raise
        


