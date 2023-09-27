from datetime import datetime

from starlette.datastructures import QueryParams

from schemas import DatetimeQueryParams


def parse_timestamp_query_params(query_params: QueryParams) -> DatetimeQueryParams:
    dp = DatetimeQueryParams()
    if "from" in query_params:
        try:
            dp.from_timestamp = datetime.fromtimestamp(int(query_params["from"]))
        except Exception:
            pass
    if "to" in query_params:
        try:
            dp.to_timestamp = datetime.fromtimestamp(int(query_params["to"]))
        except Exception:
            pass
    return dp
