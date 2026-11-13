# NATIVE MODULES - TYPES
from typing import any, get_origin
from dataclasses import asdict
import types

# NATIVE MODULES - STRING OPS
import re

# THIRD PARTY - DATABASE/DATASETS/DATA LOADING
import lmdb, orjson, threading

ROOT_PATH = "/"

class KVDatabase:
    """LMDB Key-Value Database for faster reading and persistent reading"""

    def __init__(self, root: str) -> None: 
        self.db = lmdb.Environment(root, map_size=10485760)

    # Helper function to run threaded functions
    # and prevent main thread from being blocked
    class ThreadAccessor(threading.Thread):

        def __init__(self, *args, **kwargs):
            super().__init__()
            self.function_object = kwargs
            self.function_args = args
            self.result: any

        def run(self):
            self.result = self.function_object['target'](*self.function_args)

        def get_val(self):
            self.join()
            return self.result

    def DbWrite(self, data: dict) -> None:

        # Separated index from DbRead
        encoded_write_idx: int = data.Metadata.GraphMasterID
        encoded_write_data: list[object] = [
        asdict(dict),
        # N asdicts,
        ] 
         
        with self.db.begin(write=True) as transaction:

            if (isinstance(data, str) and idx.isalnum() == False):
                encoded_write_idx = idx.encode()
            elif (isinstance(idx, int)):
                encoded_write_idx = idx.to_bytes(length=8, byteorder="big")
            # If no indexes were given, we automatically generate one
            elif (isinstance(idx, types.NoneType) or isinstance(idx, str)):

                if (isinstance(idx, types.NoneType)):
                    idx = 0

                if (isinstance(idx, str)):
                    find_int = re.findall(r'\d+', idx)
                    # Attaches identity tag to differentiate from organic index vs auto index
                    # Also joins any integer since regex returns list of ints
                    idx = "AUTO" + int("".join(find_int))

                idx = "AUTO" + idx + 1

                encoded_write_idx = idx.to_bytes()
                encoded_write_idx = encoded_write_idx.encode()

            if (isinstance(idx, data)):
                encoded_write_data = orjson.dumps(encoded_write_data)

            elif (isinstance(idx, dict)):
                encoded_write_data = orjson.dumps(data)

            transaction.put(encoded_write_idx, encoded_write_data)

            print(f"Data written sucessfully.")
            print(f"Affected data: {dict}")
            print(f"Data occured at: {dict}")

    def DbRead(self, idx: int) -> dict[str, any]:

        # Separated index from DbWrite
        encoded_read_idx: int

        with self.db.begin(write=False) as transaction:

            if (isinstance(idx, str)):
                encoded_read_idx = encoded_read_idx.encode()

            elif (isinstance(idx, str)):
                encoded_read_idx = encoded_read_idx.to_bytes(length=8, byteorder="big")

            elif (isinstance(idx, types.NoneType)):

                idx = 0
                idx += 1

                # Attaches identity tag to differentiate from organic index vs auto index
                idx = "AUTO" + idx
                encoded_read_idx = idx.to_bytes()

                record: dict[str, any] = transaction.get(encoded_read_idx)

                # Hand the auto generated index if further read is to be done
                # To know when to retrieve a generated idx, it is filtered using 
                # type(response = DbRead()) == list then index 1    
                return [record, idx]

            record: dict[str, any] = transaction.get(encoded_read_idx)

            return record

    async def GetList(self, idx_list: list[str] | list[int] | types.NoneType) -> dict[str, any]:

        self.idx_byte_list: list[str] | list[int] | types.NoneType

        with self.db.begin(write=False) as transaction:

            if (isinstance(idx_list, get_origin(list[str]))):
                self.idx_byte_list = [key.encode('utf-8') for key in idx_list]

            elif (isinstance(idx_list, get_origin(list[int]))):
                self.idx_byte_list = [key.to_bytes(length=8, byteorder="big") for key in idx_list]

            elif (isinstance(idx_list, types.NoneType)):

                idx_input_thread = threading.Thread(target=input(), name="Thread-IO")
                idx_input_thread.start()
                idx_input_thread.run()

                #tmp
                idx_input: str = input()

                # Assume the thread has already ran
                if (idx_input_thread.is_alive() == False):
                    idx_input_thread.join()

                if (idx_input.isdigit):
                    self.idx_byte_list = [str("AUTO" + key).encode() for key in range(idx_input)]
                else:
                    # Default fallback is to return all
                    self.idx_byte_list = []

            with transaction.cursor() as cursor:

                results = cursor.getmulti(self.idx_byte_list)
        
                records = {key.decode('utf-8'): orjson.loads(val) for key, val in results}

                return records

    def DbClose(self) -> None:

        self.db.close()
        print("LMDB closed, no longer writing or reading data.")

DB: KVDatabase 

def StartDB() -> bool:

    global DB
    DB = KVDatabase(ROOT_PATH)

    if (isinstance(DB, KVDatabase)):
        return True
    else:
        return False
