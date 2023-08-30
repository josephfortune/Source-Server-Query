# Written by Joe Fortune 6/6/2023

import socket
from select import select

def getServerInfo(ip_address, port):

    # ServerInfo Object
    class ServerInfo:
        valid           = True
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



    # UDP-Based Server Query
    request             = "TSource Engine Query"
    bytesToSend         = b'\xff\xff\xff\xff' + request.encode(encoding="UTF-8")
    serverAddressPort   = (ip_address, port)
    bufferSize          = 4092

    UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 

    # Send the request
    UDPSocket.sendto(bytesToSend, serverAddressPort)
    
    # Wait for the reply (or timeout)
    inputready,outputready,exceptready = select([UDPSocket],[],[], 5)
    
    if inputready:  # If reply received
        msgFromServer = UDPSocket.recvfrom(bufferSize)
    else:           # If timed out
        ServerInfo.valid = False
        return ServerInfo



    # Extract the data from the reply
    bytesString         = msgFromServer[0]

    preamble            = bytesString[0:4]

    header              = bytesString[4:5].decode("UTF-8")

    protocol            = bytesString[5:6].decode("UTF-8")

    nameStrEnd          = bytesString.find(b'\x00', 6)
    name                = bytesString[6:nameStrEnd].decode("UTF-8")

    mapStrEnd           = bytesString.find(b'\x00', nameStrEnd+1)
    map                 = bytesString[nameStrEnd:mapStrEnd].decode("UTF-8")

    folderStrEnd        = bytesString.find(b'\x00', mapStrEnd+1)
    folder              = bytesString[mapStrEnd:folderStrEnd].decode("UTF-8")

    gameStrEnd          = bytesString.find(b'\x00', folderStrEnd+1)
    game                = bytesString[folderStrEnd:gameStrEnd].decode("UTF-8")

    idStart             = gameStrEnd + 1
    idEnd               = idStart + 2
    id                  = int.from_bytes(bytesString[idStart:idEnd], byteorder="little", signed=False)

    playersStart        = idEnd
    playersEnd          = playersStart + 1
    players             = int.from_bytes(bytesString[playersStart:playersEnd], byteorder="little", signed=False)

    maxPlayersStart     = playersEnd
    maxPlayersEnd       = maxPlayersStart + 1
    maxPlayers          = int.from_bytes(bytesString[maxPlayersStart:maxPlayersEnd], byteorder="little", signed=False)

    botsStart           = maxPlayersEnd
    botsEnd             = botsStart + 1
    bots                = int.from_bytes(bytesString[botsStart:botsEnd], byteorder="little", signed=False)

    serverTypeStart     = botsEnd
    serverTypeEnd       = serverTypeStart + 1
    serverType          = bytesString[serverTypeStart:serverTypeEnd].decode("UTF-8")

    environmentStart    = serverTypeEnd
    environmentEnd      = environmentStart + 1
    environment         = bytesString[environmentStart:environmentEnd].decode("UTF-8")

    visibilityStart     = environmentEnd
    visibilityEnd       = visibilityStart + 1
    visibility          = int.from_bytes(bytesString[visibilityStart:visibilityEnd], byteorder="little", signed=False)

    vacStart            = visibilityEnd
    vacEnd              = vacStart + 1
    vac                 = int.from_bytes(bytesString[vacStart:vacEnd], byteorder="little", signed=False)

    versionStart        = vacEnd
    versionEnd          = bytesString.find(b'\x00', versionStart)
    version             = bytesString[versionStart:versionEnd].decode("UTF-8")

    extraDataFlagStart  = versionEnd
    extraDataFlagEnd    = extraDataFlagStart + 1
    extraDataFlag       = int.from_bytes(bytesString[extraDataFlagStart:extraDataFlagEnd], byteorder="little", signed=False)



    # Validate header
    if header != 'I' or preamble != b'\xFF\xFF\xFF\xFF':
        ServerInfo.valid = False
    
    # Copy the extracted data to the ServerInfo object
    ServerInfo.protocol         = protocol
    ServerInfo.name             = name
    ServerInfo.map              = map
    ServerInfo.folder           = folder
    ServerInfo.game             = game
    ServerInfo.id               = id
    ServerInfo.players          = players
    ServerInfo.maxPlayers       = maxPlayers
    ServerInfo.bots             = bots
    ServerInfo.serverType       = serverType
    ServerInfo.environment      = environment
    ServerInfo.visibility       = visibility
    ServerInfo.vac              = vac
    ServerInfo.version          = version
    ServerInfo.extraDataFlag    = extraDataFlag

    return ServerInfo


