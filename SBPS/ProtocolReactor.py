# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 0016 17:45
# @Author  : lucius
# @Email   : cnotperfect@foxmail.com
from twisted.internet import reactor, ssl
from twisted.internet.protocol import Protocol, ServerFactory
import threading
import struct
from SBPS import InternalMessage


class SBProtocol(Protocol):
    pass


class SBProtocolFactory(ServerFactory):
    '''
    ServerFactory子类
    在IotGateway中SBProtocolFactory负责维护所有客户端连接
    '''
    protocol = SBProtocol

    def __init__(self):
        self.lockDict = threading.RLock()
        self.dictRelayer = {} #K:中继器ID，V:中继器SBProtocol对象
        self.dictAccounts = {} #K:中继器ID，V:用户SBProtocol对象
    def GetAccountProtocol(self,relayer_id,client_id):
        with self.lockDict:
            if relayer_id in self.dictAccounts:
                for clientProtocol in self.dictAccounts[relayer_id]:
                    if clientProtocol.client_id==client_id:
                        return clientProtocol
        return None


def Run(withListen=True):
    '''
    gateway 通信引擎
    :return:
    '''
    instance_SBProtocolFactory = SBProtocolFactory()

    if withListen:
        reactor.listenTCP(9630, instance_SBProtocolFactory)  # 监听普通TCP端口

        cert = None

        with open('server.pem') as keyAndCert:  # 加载服务器证书
            cert = ssl.PrivateCertificate.loadPEM(keyAndCert.read())

        reactor.listenSSL(9631, instance_SBProtocolFactory, cert.option())  # 监听SSL端口
