import os
from re import search
from urllib.parse import unquote
from httpx import AsyncClient


class Auth:
    def __init__(self, accounts: os.PathLike | str) -> None:
        self.count = 0
        self.failed = 0
        self.accounts = set(open(accounts).read().splitlines())
        self.amount = len(self.accounts)
        self.client = AsyncClient()
        self.list = []

    async def xsts(self, token: str) -> tuple:
        finalized = await self.client.post(
            url="https://xsts.auth.xboxlive.com/xsts/authorize",
            json={
                "RelyingParty": "http://xboxlive.com",
                "TokenType": "JWT",
                "Properties": {
                    "UserTokens": [token],
                    "SandboxId": "RETAIL",
                },
            },
        )

        if finalized.status_code == 200:
            json = finalized.json()
            self.list.append(
                [
                    "".join(
                        [
                            "XBL3.0 x=",
                            json["DisplayClaims"]["xui"][0]["uhs"],
                            ";",
                            json["Token"],
                        ]
                    ),
                    int(json["DisplayClaims"]["xui"][0]["xid"]),
                ]
            )
        else:
            self.failed += 1
        self.count += 1

    async def combolist(self) -> tuple:
        for account in self.accounts:
            account = account.strip("\n").split(":")
            email, password = account[0], ":".join(account[1:])
            request = await self.client.get(
                url="https://login.live.com/oauth20_authorize.srf",
                params={
                    "client_id": "000000004C12AE6F",
                    "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
                    "scope": "service::user.auth.xboxlive.com::MBI_SSL",
                    "response_type": "token",
                },
            )
            if "urlPost:'" not in request.text or "sFTTag" not in request.text:
                self.count += 1
                self.failed += 1
                continue
            post_url = search(r"urlPost:'(.*?)'", request.text).group(1)
            ppft = search(r'sFTTag:\'(.*)value="(.*)"/>', request.text).groups(1)[1]
            request2 = await self.client.post(
                url=post_url,
                data={
                    "login": email,
                    "loginfmt": email,
                    "passwd": password,
                    "PPFT": ppft,
                },
            )

            if "Location" not in request2.headers:
                self.count += 1
                self.failed += 1
            else:
                token = await self.client.post(
                    url="https://user.auth.xboxlive.com/user/authenticate",
                    json={
                        "RelyingParty": "http://auth.xboxlive.com",
                        "TokenType": "JWT",
                        "Properties": {
                            "AuthMethod": "RPS",
                            "SiteName": "user.auth.xboxlive.com",
                            "RpsTicket": search(
                                "access_token=(.*)&t",
                                unquote(request2.headers["Location"]),
                            )
                            .group(1)
                            .replace("&t", ""),
                        },
                    },
                )
                await self.xsts(token.json()["Token"])
        return tuple(map(tuple, self.list)), self.failed

    async def jwt(self) -> tuple:
        [await self.xsts(token) for token in self.accounts]
        return tuple(map(tuple, self.list)), self.failed
