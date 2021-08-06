def query_param(pn: int = 1, limit: int = 20):
    if pn <= 0:
        pn = 1

    if limit > 40 or limit <= 0:
        limit = 20

    return {
        'limit': limit,
        'offset': (pn - 1) * limit
    }
