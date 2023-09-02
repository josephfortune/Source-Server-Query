
# SourceServerQuery

A Python module to retrieve and parse server information for hosted Source and GoldSrc games using the A2S_INFO and A2S_PLAYER requests
Supports Source, modern Goldsrc, and legacy Goldsrc protocols

## Usage

```python
getServerInfo(ip_address, port)
getPlayersInfo(ip_address, port)
```

### Example
```python
import SourceServerQuery

serverInfo = SourceServerQuery.getServerInfo("192.223.30.68", 27015)

if serverInfo.valid:
    print("Name:",          serverInfo.name)
    print("Protocol:",      serverInfo.protocol)
    print("Map:",           serverInfo.map)
    print("Folder:",        serverInfo.folder)
    print("Game:",          serverInfo.game)
    print("ID:",            serverInfo.id)
    print("Players:",       serverInfo.players)
    print("MaxPlayers:",    serverInfo.maxPlayers)
    print("Bots:",          serverInfo.bots)
    print("Server Type:",   serverInfo.serverType)
    print("Environment:",   serverInfo.environment)
    print("Visibility:",    serverInfo.visibility)
    print("VAC Secured:",   serverInfo.vac)
    print("Version:",       serverInfo.version)
    print("Extra Data:",    serverInfo.extraDataFlag)
	
PlayersInfo = SourceServerQuery.getPlayersInfo("192.223.30.68", 27015)

if PlayersInfo.valid:
    for player in PlayersInfo.players:
        print("Name:", 		player.name)
        print("Score:",		player.score)
        print("Duration:",	player.duration)	
```
## License

[MIT](https://choosealicense.com/licenses/mit/)

