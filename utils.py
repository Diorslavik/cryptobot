import settings


def export_cache(cache):
    cache = [str(c) for c in cache]
    data = '\n'.join(cache)
    with open(settings.CSV_FILE_NAME, 'a') as file:
        file.write(data)
