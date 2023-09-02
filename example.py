import SourceServerQuery

server_ip = "5.20.156.199"
server_port = 27015

######## ServerInfo ########
serverInfo = SourceServerQuery.getServerInfo(server_ip, server_port)

if serverInfo.valid:
    print("-----------------------------------")
    print("              Server               ")
    print("-----------------------------------")

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
else:
    print("Invalid server information")

####### PlayersInfo #######    
PlayersInfo = SourceServerQuery.getPlayersInfo(server_ip, server_port)

if PlayersInfo.valid:
    print("-----------------------------------")
    print("             Players               ")

    for player in PlayersInfo.players:
        print("-----------------------------------")
        #print("Index:", player.index)
        print("Name: \"" + player.name + "\"")
        print("Score:", player.score)
        
        # Calculate duration time
        duration    = player.duration
        
        days        = int(duration / 86400)
        hours       = int((duration - days * 86400) / 3600)
        minutes     = int(((duration - days * 86400) - hours * 3600) / 60)
        seconds     = int(((duration - days * 86400) - hours * 3600) - minutes * 60)

        timeString = ""
        if days > 0:
            timeString = f"{days}d {hours}h {minutes}m {seconds}s"
        
        elif hours > 0:
            timeString = f"{hours}h {minutes}m {seconds}s"
        
        elif minutes > 0:
            timeString = f"{minutes}m {seconds}s"
            
        else:
            timeString = f"{seconds}s"          
        print("Duration:", timeString)     
else:
    print("Invalid player information")
    
print(PlayersInfo.valid)