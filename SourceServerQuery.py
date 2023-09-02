# Written by Joe Fortune 6/6/2023

import socket
from select import select
from struct import unpack

retries = 10 # For dropped UDP packets

HEADER                          = b'\xff\xff\xff\xff'
A2S_PLAYER_REQUEST              = b'\x55'
A2S_PLAYER_RESPONSE             = b'\x44'
A2S_PLAYER_CHALLENGE_REQUEST    = b'\xff\xff\xff\xff'
A2S_CHALLENGE                   = b'\x41'
A2S_INFO_REQUEST                = "TSource Engine Query\0".encode(encoding="UTF-8")
A2S_INFO_RESPONSE               = b'\x49'
A2S_INFO_RESPONSE_OLD           = b'\x6d'
A2S_SERVERQUERY_GETCHALLENGE    = b'\x57'   # Old goldsrc games only



def getPlayersInfo(ip_address, port):

    # Player Object
    class Player:
        index       = "Unknown"
        name        = "Unknown"
        score       = "Unknown"
        duration    = "Unknown" #seconds 
    
    # PlayersInfo Object
    class PlayersInfo:
        valid           = False
        players         = []
        playerCount     = "Unknown"
        
    info = PlayersInfo()
        
    # UDP-Based Server Query
    bytesToSend         = HEADER + A2S_PLAYER_REQUEST + A2S_PLAYER_CHALLENGE_REQUEST
    reply               = sendRequest(ip_address, port, bytesToSend, retries)
    
    # Is the server issuing the challenge string (modern method)?
    if reply[0:5] == HEADER + A2S_CHALLENGE:
        challengeString = reply[5:9]
        bytesToSend     = HEADER + A2S_PLAYER_REQUEST + challengeString
        reply           = sendRequest(ip_address, port, bytesToSend, retries)  
    
    # Otherwise will the server respond to the old Goldsrc challenge method?
    else:
        bytesToSend     = HEADER + A2S_SERVERQUERY_GETCHALLENGE
        reply           = sendRequest(ip_address, port, bytesToSend, retries)
        
        if reply[0:5] == HEADER + A2S_CHALLENGE:
            challengeString = reply[5:9]
            bytesToSend     = HEADER + A2S_PLAYER_REQUEST + challengeString
            reply           = sendRequest(ip_address, port, bytesToSend, retries)
    
    # Recieve data
    if reply[0:5] != HEADER + A2S_PLAYER_RESPONSE:
        info.valid   = False
        return info
    
    # Player count
    info.playerCount = reply[5]
    
    # For each player
    playerChunkOffset = 6
    for playerIndex in range(info.playerCount):
        currentPlayer       = Player()
        currentPlayer.index = reply[playerChunkOffset]
        
        # Name
        stringStart             = playerChunkOffset + 1
        stringEnd               = reply.find(b'\x00', stringStart) 
        currentPlayer.name      = reply[stringStart : stringEnd].decode("UTF-8")
        
        # Score
        scoreStart              = stringEnd + 1
        scoreEnd                = scoreStart + 4
        currentPlayer.score     = int.from_bytes(reply[scoreStart:scoreEnd], byteorder="little", signed=True)
        
        # Duration
        durationStart           = scoreEnd
        durationEnd             = durationStart + 4
        currentPlayer.duration  = unpack('<f', reply[durationStart:durationEnd])[0]
               
        info.players.append(currentPlayer)
        playerChunkOffset   = stringEnd + 1 + 8 # Update chunk offset to start of next player
    
    info.valid = True
    return info
    
    
    
def getServerInfo(ip_address, port):

    # ServerInfo Object
    class ServerInfo:
        valid           = False
        protocol        = "Unknown"
        name            = "Unknown"
        map             = "Unknown"
        folder          = "Unknown"
        game            = "Unknown"
        id              = "Unknown"
        players         = "Unknown"
        maxPlayers      = "Unknown"
        bots            = "Unknown"
        serverType      = "Unknown"
        environment     = "Unknown"
        visibility      = "Unknown"
        vac             = "Unknown"
        version         = "Unknown"
        extraDataFlag   = "Unknown"

    info = ServerInfo()


    # UDP-Based Server Query
    bytesToSend         = HEADER + A2S_INFO_REQUEST
    reply = sendRequest(ip_address, port, bytesToSend, retries)
    
    # Is server requesting challenge string?
    if reply[:5] == HEADER + A2S_CHALLENGE:
        challenge = reply[5:9]
        reply = sendRequest(ip_address, port, bytesToSend + challenge, retries)
    
    # Validate header
    if reply[:5] == HEADER + A2S_INFO_RESPONSE: # Modern steam header

        # Extract the data from the reply
        preamble            = reply[0:4]

        header              = reply[4:5].decode("UTF-8")

        protocol            = reply[5:6].decode("UTF-8")

        nameStrEnd          = reply.find(b'\x00', 6)
        name                = reply[6:nameStrEnd].decode("UTF-8")

        mapStrEnd           = reply.find(b'\x00', nameStrEnd+1)
        map                 = reply[nameStrEnd:mapStrEnd].decode("UTF-8")

        folderStrEnd        = reply.find(b'\x00', mapStrEnd+1)
        folder              = reply[mapStrEnd:folderStrEnd].decode("UTF-8")

        gameStrEnd          = reply.find(b'\x00', folderStrEnd+1)
        game                = reply[folderStrEnd:gameStrEnd].decode("UTF-8")

        idStart             = gameStrEnd + 1
        idEnd               = idStart + 2
        id                  = int.from_bytes(reply[idStart:idEnd], byteorder="little", signed=False)

        playersStart        = idEnd
        playersEnd          = playersStart + 1
        players             = int.from_bytes(reply[playersStart:playersEnd], byteorder="little", signed=False)

        maxPlayersStart     = playersEnd
        maxPlayersEnd       = maxPlayersStart + 1
        maxPlayers          = int.from_bytes(reply[maxPlayersStart:maxPlayersEnd], byteorder="little", signed=False)

        botsStart           = maxPlayersEnd
        botsEnd             = botsStart + 1
        bots                = int.from_bytes(reply[botsStart:botsEnd], byteorder="little", signed=False)

        serverTypeStart     = botsEnd
        serverTypeEnd       = serverTypeStart + 1
        serverType          = reply[serverTypeStart:serverTypeEnd].decode("UTF-8")

        environmentStart    = serverTypeEnd
        environmentEnd      = environmentStart + 1
        environment         = reply[environmentStart:environmentEnd].decode("UTF-8")

        visibilityStart     = environmentEnd
        visibilityEnd       = visibilityStart + 1
        visibility          = int.from_bytes(reply[visibilityStart:visibilityEnd], byteorder="little", signed=False)

        vacStart            = visibilityEnd
        vacEnd              = vacStart + 1
        vac                 = int.from_bytes(reply[vacStart:vacEnd], byteorder="little", signed=False)

        versionStart        = vacEnd
        versionEnd          = reply.find(b'\x00', versionStart)
        version             = reply[versionStart:versionEnd].decode("UTF-8")

        extraDataFlagStart  = versionEnd
        extraDataFlagEnd    = extraDataFlagStart + 1
        extraDataFlag       = int.from_bytes(reply[extraDataFlagStart:extraDataFlagEnd], byteorder="little", signed=False)
        
        # Copy the extracted data to the ServerInfo object
        info.protocol         = protocol
        info.name             = name
        info.map              = map
        info.folder           = folder
        info.game             = game
        info.id               = id
        info.players          = players
        info.maxPlayers       = maxPlayers
        info.bots             = bots
        info.serverType       = serverType
        info.environment      = environment
        info.visibility       = visibility
        info.vac              = vac
        info.version          = version
        info.extraDataFlag    = extraDataFlag
        info.valid = True
    
    elif reply[:5] == HEADER + A2S_INFO_RESPONSE_OLD: # Old goldsrc header
        
        # Extract the data from the reply
        preamble            = reply[0:4]

        header              = reply[4:5].decode("UTF-8")
        
        ipStrEnd            = reply.find(b'\x00', 5)
        ip                  = reply[5:ipStrEnd].decode("UTF-8")
        
        nameStrEnd          = reply.find(b'\x00', ipStrEnd+1)
        name                = reply[ipStrEnd+1:nameStrEnd].decode("UTF-8")
        
        mapStrEnd           = reply.find(b'\x00', nameStrEnd+1)
        map                 = reply[nameStrEnd+1:mapStrEnd].decode("UTF-8")
        
        folderStrEnd        = reply.find(b'\x00', mapStrEnd+1)
        folder              = reply[mapStrEnd+1:folderStrEnd].decode("UTF-8")
        
        gameStrEnd          = reply.find(b'\x00', folderStrEnd+1)
        game                = reply[folderStrEnd+1:gameStrEnd].decode("UTF-8")
        
        players, maxPlayers, protocol, serverType, environment, visibility, mod = unpack('sssssss', reply[gameStrEnd:gameStrEnd+7])
        
        
        info.name           = name
        info.map            = map
        info.folder         = folder
        info.game           = game
        info.players        = players
        info.maxPlayers     = maxPlayers
        info.protocol       = protocol
        info.serverType     = serverType
        info.environment    = environment
        info.visibility     = visibility  
        info.valid          = True

    return info



lastIPAddress = "none"
UDPSocket = 0
def sendRequest(ipAddress, port, data, retry):

    global lastIPAddress
    global UDPSocket
    timeOut = 1
    bufferSize = 4092

    if ipAddress != lastIPAddress: # New conection, need to initialize the socket
        lastIPAddress = ipAddress
        UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)   
    
    UDPSocket.sendto(data, (ipAddress, port))
    
    # Wait for the reply (or timeout)
    inputready,outputready,exceptready = select([UDPSocket],[],[], timeOut)
    
    if inputready:  # If reply received
        reply = UDPSocket.recvfrom(bufferSize)[0]
    
    else:           # If timed out
        if retry > 0:
            #print("Timed out: Retrying...", retry)
            reply = sendRequest(ipAddress, port, data, retry - 1) # Retry
        else:
            reply = b''
 
    return reply