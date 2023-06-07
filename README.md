
# SourceServerQuery

A Python module to retrieve and parse server information for hosted Source and GoldSrc games using the A2S_INFO request


## Usage

```python
getServerInfo(ip_address, port)
```
Queries the server and returns a ServerInfo object

### Example
```python
import ServerQuery
ServerInfo = ServerQuery.getServerInfo("192.223.30.68", 27015)

if ServerInfo.valid:
    print("Name: "          + ServerInfo.name           + "\n")
    print("Protocol: "      + ServerInfo.protocol       + "\n")
    print("Folder: "        + ServerInfo.folder         + "\n")
    print("Game: "          + ServerInfo.game           + "\n")
    print("ID: "            + ServerInfo.id             + "\n")
    print("Players: "       + ServerInfo.players        + "\n")
    print("MaxPlayers: "    + ServerInfo.maxPlayers     + "\n")
    print("Bots: "          + ServerInfo.bots           + "\n")
    print("Server Type: "   + ServerInfo.serverType     + "\n")
    print("Environment: "   + ServerInfo.environment    + "\n")
    print("Visibility: "    + ServerInfo.visibility     + "\n")
    print("VAC Secured: "   + ServerInfo.vac            + "\n")
    print("Version: "       + ServerInfo.version        + "\n")
    print("Extra Data: "    + ServerInfo.extraDataFlag  + "\n")
```
## License

[MIT](https://choosealicense.com/licenses/mit/)

