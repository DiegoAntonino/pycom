import gc
import pycom


def init_gc():
    '''
    Eanble GC and run it automatically when the allocated heap memory is
    over the 85% of the total heap memory
    '''
    if not gc.isenabled():
        gc.enable()
    gc.threshold(int((gc.mem_free() + gc.mem_alloc()) * 0.85))
    gc.collect()

#MAIN
init_gc()
pycom.heartbeat(False)
