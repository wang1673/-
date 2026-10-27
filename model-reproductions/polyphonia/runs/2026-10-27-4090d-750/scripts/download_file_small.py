from download_file import download as original

def download(url,output,checksum=None,workers=6):
    return original(url,output,checksum,workers=workers,chunk_size=1024**2,parts_suffix='.parts1m')
