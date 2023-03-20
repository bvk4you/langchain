"""Lightweight wrapper around requests library, with async support."""
from typing import Any, Dict, Optional
import warnings
import aiohttp
import requests
from urllib3.exceptions import InsecureRequestWarning
from pydantic import BaseModel, Extra


class RequestsWrapper(BaseModel):
    """Lightweight wrapper around requests library."""

    headers: Optional[Dict[str, str]] = None
    aiosession: Optional[aiohttp.ClientSession] = None
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    def get(self, url: str) -> str:
        """GET the URL and return the text."""
        return requests.get(url, headers=self.headers,verify=False).text

    def post(self, url: str, data: Dict[str, Any]) -> str:
        """POST to the URL and return the text."""
        return requests.post(url, json=data, headers=self.headers,verify=False).text

    def patch(self, url: str, data: Dict[str, Any]) -> str:
        """PATCH the URL and return the text."""
        return requests.patch(url, json=data, headers=self.headers).text

    def put(self, url: str, data: Dict[str, Any]) -> str:
        """PUT the URL and return the text."""
        return requests.put(url, json=data, headers=self.headers,verify=False).text

    def delete(self, url: str) -> str:
        """DELETE the URL and return the text."""
        return requests.delete(url, headers=self.headers).text

    async def _arequest(self, method: str, url: str, **kwargs: Any) -> str:
        """Make an async request."""
        if not self.aiosession:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method, url, headers=self.headers,ssl=False **kwargs
                ) as response:
                    return await response.text()
        else:
            async with self.aiosession.request(
                method, url, headers=self.headers,ssl=False,**kwargs
            ) as response:
                return await response.text()

    async def aget(self, url: str) -> str:
        """GET the URL and return the text asynchronously."""
        return await self._arequest("GET", url)

    async def apost(self, url: str, data: Dict[str, Any]) -> str:
        """POST to the URL and return the text asynchronously."""
        return await self._arequest("POST", url, json=data)

    async def apatch(self, url: str, data: Dict[str, Any]) -> str:
        """PATCH the URL and return the text asynchronously."""
        return await self._arequest("PATCH", url, json=data)

    async def aput(self, url: str, data: Dict[str, Any]) -> str:
        """PUT the URL and return the text asynchronously."""
        return await self._arequest("PUT", url, json=data)

    async def adelete(self, url: str) -> str:
        """DELETE the URL and return the text asynchronously."""
        return await self._arequest("DELETE", url)
