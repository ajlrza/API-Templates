from contextlib import contextmanager
from typing import NamedTuple, Literal
from collections import abc

import os, multiprocessing, asyncio

CPU_LEVELS: set[str] = ["ONE_CORE", "MULTIPLE_CORES"]
STATE_PARTITION_POOL_PATH: str = "/partition/"
BUFFER_CLEARANCE_COUNT = 50

class state_partition(NamedTuple):
    partition_name: str
    partition_priority: Literal["HIGH", "MEDIUM", "LOW"]
    partition_data: list[dict]
    partition_status: Literal["UP", "DOWN"]

class state_partition_info(NamedTuple):
    active_partitions: list[state_partition]
    partition_count: int

state_hypervisor_buffer: asyncio.Queue = asyncio.Queue(maxsize=100)
state_partition_pool: dict[str, state_partition] 
partition_central_management: state_partition_info = state_partition_info()

def CpuStatsConfigurator() -> bool:

    global CPU_ACTIVE
    global GPU_ACTIVE
    global PID
    global current
    global children
    global CPU_COUNT
    global CPU_LEVEL
    
    CPU_ACTIVE = True
    GPU_ACTIVE= False
    PID: int = os.getpid
    current = multiprocessing.current_process()
    children = multiprocessing.active_children()
    CPU_COUNT = os.cpu_count() or 1

    if (CPU_COUNT == 1):
        print("Using default system level...")
        CPU_LEVEL = "ONE_CORE"

    elif (CPU_COUNT > 1):
        print(f"Multiple cores detected, setting CPU_LEVEL to {"MULTPLE_CORES"}")
        CPU_LEVEL = "MULTIPLE_CORES"

    return True

def CreateStatePartition(partition_name: str, partition_count: int = 0) -> None:

    partition = state_partition()
    partition.partition_name = partition_name
    partition_central_management.partition_count = partition_count

def SendToPartition(partition_name, data):

    with open(f'{STATE_PARTITION_POOL_PATH}/{partition_name}.txt', 'w') as file:
        file.write(data)

    partition_central_management.partition_count += 1

def EnqueueStateData(partition_name, data):

    sent_to_queue = state_hypervisor_buffer.put(SendToPartition(partition_name, data))
    return sent_to_queue

async def DequeueForSending() -> bool:

    current_queue_count = state_hypervisor_buffer.qsize()

    current_partition_executed = await state_hypervisor_buffer.get()
    await current_partition_executed

    state_hypervisor_buffer.task_done()

    if (current_queue_count - 1 == state_hypervisor_buffer.qsize()):
        partition_central_management.partition_count -= 1
        return True
    else:
        return False

def SendMainStates(payload: list[dict]):

    sent_state_data = EnqueueStateData('OBSERVED', payload)
    return sent_state_data

def SendBackgroundStates(payload: list[dict]):

    sent_state_data = EnqueueStateData('UNOBSERVED', payload)
    return sent_state_data

def SendMiscStates(payload: list[dict]):

    sent_state_data = EnqueueStateData('MISC', payload)
    return sent_state_data

@contextmanager
async def Monitor():

    global buffer_clearance_count

    while (state_hypervisor_buffer.empty() == False):
      dequeuing = await DequeueForSending() 
      buffer_clearance_count -= 1

    if (buffer_clearance_count != 0):
        print("Remaining count uncleared: " + buffer_clearance_count)
        return
