---
name: Dash Discord
description: Discord integration for the Dash framework.
endpoint: /pip/dash_discord
package: dash_discord
icon: uim:discord
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/Dash_Discord)

### Installation

```bash
pip install dash-discord
```

### Introduction

Their are two components in this package `DiscordCrate` and `DiscordWidget`.

`DiscordCrate` is a collapsable and expandable widget that allows users to interact with a Discord server.

`DiscordWidget` is a full screen always open widget that allows users to interact with a Discord server.

.. exec::docs.dash_discord.introduction

### DiscordWidget Props

| Prop       | Description                                                                                |
|------------|--------------------------------------------------------------------------------------------|
| `server`   | Required String. Found in the discord server settings.                                     |
| `channel`  | Required String. Found right clicking the channel you want to connect with and copy the ID |
| `username` | Optional String. Initial username to show by default.                                      |
| `avatar`   | Optional String. URL of the users avatar to show by default.                               |
| `hight`    | Optional String. On load height of the component.                                          |
| `width`    | Optional String. On load width of the component.                                           |


### DiscordCrate Props
A `DiscordCrate` is a collapsable and expandable widget that allows users to interact with a Discord server. It can be used to display a Discord server in a Dash app.

.. exec::docs.dash_discord.crate_images
    :code: false

```python
from dash import Dash, html
from dash_discord import DiscordCrate

DiscordCrate(
    id='crate',
    server='1246197743307980940',
    channel='1246197743781810332',
    username='Pip Install Python',
    avatar='https://avatars.githubusercontent.com/u/83238564',
    location=['top', 'left'],
    color='red',
    glyph=['https://geomapindex.com/media/blog_qr/2024/05/28/qr-http___dashgeomapindexcom_AihBuSf.gif', '75px'],
    notifications=True,
    indicator=True,
    timeout=5000,
    allChannelNotifications=True,
    embedNotificationTimeout=5000,
    defer=True,
)
```

| Prop                       | Description                                                                                                                                       |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `server`                   | Required String. Found in the discord server settings.                                                                                            |
| `channel`                  | Required String. Found right clicking the channel you want to connect with and copy the ID                                                        |
| `username`                 | Optional String. Initial username to show by default.                                                                                             |
| `avatar`                   | Optional String. URL of the users avatar to show by default.                                                                                      |
| `location`                 | Optional List. Two items in the list to describe positioning of the Crate for example: ['top', 'right'], ['bottom', 'left'], exc.                 |
| `color`                    | Optional String. Used to change the color of the crate button.                                                                                    |
| `glyph`                    | Optional String. Url or gif used to render on top of the crate.                                                                                   |
| `notifications`            | Optional Boolean. Whether to show notifications on the crate.                                                                                     |
| `indicator`                | Optional Boolean. Crate unread message indicator                                                                                                  |
| `timeout`                  | Optional Number. When crate notification timeout                                                                                                  |
| `allChannelNotifications`  | Optional Boolean. Send notifications for all channels.                                                                                            |
| `embedNotificationTimeout` | Optional Number. Amount of time till Notification alerts are set to time out.                                                                     |
| `defer`                    | Optional Boolean. Whether to preload the resource or not |

