# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Bounded read-only local Modbus TCP. No discovery, writes or actuation."""
from .core import Result,ValidationError,ConsentRequired,require

def modbus_read(*,host,address,count,config,port=502,device_id=1):
    if not config.allow_network:raise ConsentRequired('Modbus read requires explicit allow_network=True')
    if host not in ('127.0.0.1','localhost','::1'):raise ConsentRequired('This adapter only supports loopback testing/local gateways; remote plaintext Modbus is deliberately disabled')
    if type(address)is not int or type(count)is not int or not 0<=address<=65535 or not 1<=count<=125 or address+count>65536 or type(port)is not int or not 1<=port<=65535 or type(device_id)is not int or not 0<=device_id<=247:raise ValidationError('Invalid Modbus address/count/port/device ID')
    cls=require('pymodbus.client','industrial').ModbusTcpClient
    client=cls(host,port=port,timeout=min(config.timeout,10),retries=0)
    try:
        if not client.connect():raise ValidationError('Cannot connect to explicitly chosen Modbus endpoint')
        reply=client.read_holding_registers(address,count=count,device_id=device_id)
        if reply.isError():raise ValidationError('Modbus endpoint returned an error')
        values=list(reply.registers)
    finally:client.close()
    return Result('iot.modbus.read',{'address':address,'device_id':device_id,'registers':values,'rows':[{'address':address+i,'raw_uint16':v} for i,v in enumerate(values)]},'pymodbus.tcp-read-only',['Raw 16-bit registers; scaling, signedness, byte order and engineering units are device-specific. Local server verification is not physical PLC validation.'])
