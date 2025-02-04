import logging

from requests import request, exceptions

logger = logging.getLogger(__name__)


class BaseClient:
    base_url = None

    def _request(self, method: str,
                    params: dict = None,  # noqa
                    headers: dict = None,  # noqa
                    data: dict = None,  # noqa
                    url: str = None) -> dict or bytes:  # noqa
        try:
            response = request(
                url=url or self.base_url,
                method=method,
                params=params or {},
                data=data or {},
                headers=headers or {}
            )
            json_response = response.json()
        except (exceptions.ConnectionError, exceptions.Timeout) as error:
            logger.error(error)
        except exceptions.JSONDecodeError:
            return response.content
        else:
            return json_response
