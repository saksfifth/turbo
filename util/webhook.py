from httpx import Client


class webhookexception(Exception):
    pass


class Webhook:
    def __init__(self, vars) -> None:
        self.vars, self.webhooks = vars, [
            {
                "url": "https://canary.discord.com/api/webhooks/1162566916611788890/w5WB-97nVGndp9RR5o_sW_rSv9oaTAuSjU2tqXeSCGjAiDyGX5kKMYPnX7wElI5-lPWU", # set webhook url here
                "method": "POST",
                "headers": {},
                "params": {},
                "json": {
                    "content": "<@!1032062115973976125>",
                    "embeds": [
                        {
                            "title": "Successful Turbo!",
                            "color": None,
                            "fields": [
                                {
                                    "name": "`Gamertag`",
                                    "value": f"`{vars['tag']}`",
                                    "inline": True
                                },
                                {
                                    "name": "`XUID`",
                                    "value": f"`{vars['new_account'][1]}`",
                                    "inline": True
                                },
                                {
                                    "name": "`Requests`",
                                    "value": f"`{vars['requests']}`",
                                    "inline": True
                                }
                            ]
                        }
                    ],
                    "attachments": []
                },
                "success_code": 204
            }
        ]

    async def push(self):
        client = Client()
        methods = {"GET": client.get, "POST": client.post, "PUT": client.put, "PATCH": client.patch,
                       "DELETE": client.delete}
        for webhook in self.webhooks:
                try:
                    x = methods.get(webhook.get('method'))(url=webhook.get('url'), headers=webhook.get('headers'), params=webhook.get('params'), json=webhook.get("json"))
                    if x.status_code == webhook["success_code"]:
                            print(f"Sent to webhook | {webhook['url']}")
                    else:
                            print(f"Failed sending webhook according to status_code | {webhook['url']}")
                except Exception as e:
                    raise webhookexception from e
