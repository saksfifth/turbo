from random import uniform
from datetime import datetime
from asyncio import sleep
from httpx import AsyncClient, Request
from rich.console import Console
from util import Webhook, webhookexception, center_y

class Turbo:
    def __init__(self) -> None:
        (
            self.reservation,
            self.claim,
            self.requests,
            self.ratelimits,
            self.errors,
            self.claimed,
            self.console,
            self.accounts,
            self.threads,
            self.tag,
            self.rd,
            self.cd,
            self.new_account,
            self.banner,
            self.rs,
        ) = (
            "https://gamertag.xboxlive.com/gamertags/reserve",
            "https://accounts.xboxlive.com/users/current/profile/gamertag",
            0,
            0,
            0,
            False,
            Console(),
            [],
            None,
            None,
            {},
            {},
            None,
            """
૮⍝• ᴥ •⍝ა
८ › ༝ ‹ ა 
૮꒰ྀི⊃⸝ ⸝ ⸝⊂꒱ྀིა
૮꒰ྀི∩´ ᵕ `∩꒱ྀིა
૮꒰ྀི ´∩∩` ꒱ྀིა
໒꒰ྀི∩˃ ᵕ ˂∩꒱ྀི১
໒꒰ ྀི ⸝⸝⸝ ꒱ა
૮꒰⸝⸝> ̫ <⸝⸝꒱ა
૮꒰ ˶> ༝ <˶꒱ა
໒꒰ྀི ˊᗜˋ* ꒱ྀིა
""",
            0,
        )

    async def request_hook(self, request: Request):
        self.requests += 1

    async def save_info(self, type: int, **kwargs) -> None:
        if type == 0:
            with open("data/claimed.txt", "a+") as w:
                w.write(
                    f"[{kwargs['date']}] -> [{kwargs['xuid']}] | [{kwargs['reservation']}] | [{kwargs['email']}] | -> [{self.tag}]\n"
                )
        elif type == 1:
            with open("data/reserved.txt", "a+") as w:
                w.write(
                    f"[{kwargs['date']}] -> [{kwargs['xuid']}] | [{kwargs['email']}] -> [{self.tag}] | [{kwargs['reservation']}]\n"
                )

    async def success(self, opttext="") -> None:
        [self.console.clear() for _ in range(10)]
        self.console.print(
            f"{center_y()}[bold grey93]{self.banner}[/bold grey93]\n[[bold grey85]*[/bold grey85]] Request(s): [bold grey85]{self.requests}[/bold grey85] | R/s: [bold grey85]{self.rs}[/bold grey85] | RL(s): [bold grey85]{self.ratelimits}[/bold grey85] | Errors: [bold grey85]{self.errors}[/bold grey85] | Threads: [bold grey85]{self.threads}[/bold grey85]\n\n[[bold grey85]*[/bold grey85]] Claimed: {self.tag}\n[[bold grey85]*[/bold grey85]] Email: {self.new_account[0]}\n[[bold grey85]*[/bold grey85]] XUID: {self.new_account[1]}\n{opttext}",
            end=(" " * 24) + "\n",
            highlight=False,
            justify="center",
        )
        try:
            await Webhook(vars(self)).push()
        except webhookexception:
            self.console.print(
                "[[bold grey85]-[/bold grey85]] Failed sending message to webhook(s)",
                end=(" " * 24) + "\n",
                highlight=False,
            )
        input()
        exit(0)

    async def whatdoinamethis(self, session: AsyncClient, token, resid, xuid, mscv) -> None:
        request = await session.post(
            url=self.reservation,
            headers={
                "MS-CV": mscv,
                "x-xbl-contract-version": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                "Authorization": token,
            },
            json={
                "gamertag": self.tag,
                "targetGamertagFields": "gamertag",
                "reservationId": resid,
            }
        )
        if request.status_code == 200:
            await self.claimgt(
                session,
                token,
                resid,
                xuid,
                mscv,
                "[[bold grey85]*[/bold grey85]] Had to use new gamertag system sorry :/",
            )
        elif request.status_code == 429:
            self.ratelimits += 1
            await sleep(request.json()["periodInSeconds"])
            await self.whatdoinamethis(session, token, resid, xuid, mscv)
        else:
            self.errors += 1

    async def uuiderrorthing(
        self, session: AsyncClient, token, resid, xuid, mscv
    ) -> None:
        request = await session.post(
            url=self.reservation,
            headers={
                "MS-CV": mscv,
                "x-xbl-contract-version": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                "Authorization": token,
            },
            json={**self.rd, "reservationId": resid},
        )
        if request.status_code == 200:
            if request.json()["classicGamertag"] == self.tag:
                claim = await session.post(
                    self.claim,
                    headers={
                        "MS-CV": mscv,
                        "x-xbl-contract-version": "6",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                        "Authorization": token,
                    },
                    json={
                        "reservationId": 0,
                        "gamertag": "",
                        "preview": True,
                        "useLegacyEntitlement": False,
                    },
                )
                if (
                    claim.status_code == 200
                    and claim.json()["hasModernGamertag"] is False
                ) and len(self.tag) <= 12:
                    self.cd = {
                        "gamertag": {
                            "gamertag": self.tag,
                            "gamertagSuffix": "",
                            "classicGamertag": self.tag,
                        },
                        "preview": False,
                        "useLegacyEntitlement": False,
                    }
                    await self.whatdoinamethis(session, token, resid, xuid, mscv)
                else:
                    self.claimed = True
                    date = datetime.now()
                    await self.save_info(
                        1,
                        xuid=xuid,
                        reservation=resid,
                        email=(
                            await session.get(
                                "https://accounts.xboxlive.com/users/current/profile",
                                headers={
                                    "Authorization": token,
                                    "x-xbl-contract-version": "1",
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                                },
                            )
                        ).json()["email"],
                        date=date,
                    )
                    self.console.clear()
                    self.console.print(
                        f"{center_y()}[bold grey93]{self.banner}[/bold grey93]\n\nCouldn't claim [bold grey85]{self.tag}[/bold grey85] but managed to reserve it | Reservation ID: [bold grey85]{resid}[/bold grey85]\nTime when [bold grey85]{self.tag}[/bold grey85] was reserved: [bold grey85]{date}[/bold grey85] (Expires in 1 hour)",
                        justify="center",
                        highlight=False,
                    )
            elif request.status_code == 429:
                await sleep(request.json()["periodInSeconds"])
                await self.uuiderrorthing(session, token, resid, xuid, mscv)
            else:
                self.errors += 1

    async def info(self) -> None:
        while self.claimed is False:
            rn = self.requests
            await sleep(1)
            self.rs = self.requests - rn
            self.console.print(
                f"[[bold grey85]*[/bold grey85]] Request(s): [bold grey85]{self.requests}[/bold grey85] | R/s: [bold grey85]{self.rs}[/bold grey85] | Errors: [bold grey85]{self.errors+self.ratelimits}[/bold grey85] | Gamertag: [bold grey85]{self.tag}[/bold grey85]",
                end="\r",
                highlight=False,
            )
        exit(0)

    async def claimgt(
        self,
        session: AsyncClient,
        token: str,
        resid: str,
        xuid: str,
        mscv: str,
        opttext: str = "",
    ):
        request = await session.post(
            self.claim,
            headers={
                "MS-CV": mscv,
                "Authorization": token,
                "x-xbl-contract-version": "6",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            },
            json={**self.cd, "reservationId": resid},
        )
        if request.status_code == 200:
            self.claimed = True
            email = (
                    await session.get(
                        "https://accounts.xboxlive.com/users/current/profile",
                        headers={
                            "Authorization": token,
                            "x-xbl-contract-version": "1",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                        },
                    )
                ).json()["email"]
            self.new_account = [email, xuid]
            await self.save_info(
                0,
                xuid=xuid,
                reservation=resid,
                email=email,
                date=datetime.now(),
            )
            await self.success(opttext)
            
        elif request.status_code == 429:
            self.ratelimits += 1
        elif request.status_code == 403:
            if (
                request.json()["code"] == 5025
                and request.json()["description"]
                == "272abc3c-8b49-469f-b589-72eaa902fa64"
            ):
                await self.uuiderrorthing(session, token, resid, xuid, mscv)
        else:
            self.errors += 1

    async def reserve(self) -> None:
        session = AsyncClient(event_hooks={'request': [self.request_hook]}, verify=False)
        while self.claimed is False:
            try:
                for token, xuid in self.accounts:
                    resid = uniform(xuid * 2, xuid * 4).__round__().__str__()
                    request = await session.post(
                        url=self.reservation,
                        headers={
                            "x-xbl-contract-version": "1",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                            "Authorization": token,
                        },
                        json={**self.rd, "reservationId": resid},
                    )
                    if request.status_code == 200:
                        if request.json()["classicGamertag"] == self.tag:
                            await self.claimgt(
                                session, token, resid, xuid, request.headers["MS-CV"]
                            )
                    elif request.status_code == 429:
                        self.ratelimits += 1
                    elif request.status_code != 409:
                        self.errors += 1
            except Exception as e:
                print(e)
        exit(0)
