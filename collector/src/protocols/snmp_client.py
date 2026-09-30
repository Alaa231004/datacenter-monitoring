from datetime import datetime
import asyncio

from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    get_cmd
)


class SNMPClient:

    CPU_OID = "1.3.6.1.4.1.2021.11.9.0"
    RAM_OID = "1.3.6.1.4.1.2021.4.6.0"
    TEMP_OID = "1.3.6.1.4.1.2021.13.16.2.1.3.1"

    DISK_OID = "1.3.6.1.4.1.2021.9.1.0"
    POWER_OID = "1.3.6.1.4.1.2021.10.1.0"
    NETWORK_IN_OID = "1.3.6.1.4.1.2021.11.1.0"
    NETWORK_OUT_OID = "1.3.6.1.4.1.2021.11.2.0"
    FAN_SPEED_OID = "1.3.6.1.4.1.2021.12.1.0"

    @staticmethod
    async def get_value(ip, port, community, oid):

        transport = await UdpTransportTarget.create(
            (ip, port),
            timeout=3,
            retries=1
        )

        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            SnmpEngine(),
            CommunityData(community, mpModel=1),
            transport,
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )

        print("errorIndication =", errorIndication)
        print("errorStatus =", errorStatus)
        print("varBinds =", varBinds)

        if errorIndication:
            raise Exception(errorIndication)

        if errorStatus:
            raise Exception(errorStatus.prettyPrint())

        return int(varBinds[0][1])

    @staticmethod
    def collect(equipment):

        cpu = asyncio.run(
            SNMPClient.get_value(
                equipment.ip,
                equipment.port,
                equipment.community,
                SNMPClient.CPU_OID
            )
        )

        ram = asyncio.run(
            SNMPClient.get_value(
                equipment.ip,
                equipment.port,
                equipment.community,
                SNMPClient.RAM_OID
            )
        )

        temperature = asyncio.run(
            SNMPClient.get_value(
                equipment.ip,
                equipment.port,
                equipment.community,
                SNMPClient.TEMP_OID
            )
        )

        disk = asyncio.run(
            SNMPClient.get_value(
                equipment.ip,
                equipment.port,
                equipment.community,
                SNMPClient.DISK_OID
            )
        )

        power = asyncio.run(
            SNMPClient.get_value(
                equipment.ip,
                equipment.port,
                equipment.community,
                SNMPClient.POWER_OID
            )
        )

        network_in = asyncio.run(
            SNMPClient.get_value(
                equipment.ip,
                equipment.port,
                equipment.community,
                SNMPClient.NETWORK_IN_OID
            )
        )

        network_out = asyncio.run(
            SNMPClient.get_value(
                equipment.ip,
                equipment.port,
                equipment.community,
                SNMPClient.NETWORK_OUT_OID
            )
        )

        fan_speed = asyncio.run(
            SNMPClient.get_value(
                equipment.ip,
                equipment.port,
                equipment.community,
                SNMPClient.FAN_SPEED_OID
            )
        )

        # ==========================
        # Déterminer le statut
        # ==========================

        if cpu > 90 or temperature > 42:
            status = "CRITICAL"

        elif cpu > 75 or temperature > 38:
            status = "WARNING"

        else:
            status = "OK"

        return {
            "equipment_id": equipment.id,
            "hostname": equipment.hostname,
            "type": equipment.type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "temperature": temperature,
            "power": power,
            "network_in": network_in,
            "network_out": network_out,
            "fan_speed": fan_speed,
            "status": status
        }
