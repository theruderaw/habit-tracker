from src.db import get_db

class TableNotGiven(Exception):
    pass

def execute_query(query: str, params: dict = None):

    try:
        with get_db() as db:
            if params:
                db.execute(query, tuple(params.values()))
            else:
                db.execute(query)
    except Exception as e:
        print(f"Failed because of {e}")

def paginate(params):
    page = params.get("page_no", 1)
    size = params.get("page_size", 10)
    return {
        **{k: v for k, v in params.items() if k not in ("page_no", "page_size")},
        "offset": (page-1)*size,
        "limit": size
    }

def fetch_query( params):
    filters = params.get("filters", {})
    columns = params.get("rows", "*")
    query = f"SELECT {','.join(columns)} FROM habits"
    filter_clauses = []
    values = []
    for col, cond in filters.items():
        filter_clauses.append(f"{col} {cond['op']} ?")
        values.append(cond["val"])
    params = paginate(params)
    filter_clause = " WHERE " + " AND ".join(filter_clauses) if filter_clauses else ""
    query += filter_clause
    query += f" LIMIT {params['limit']} OFFSET {params['offset']}"
    with get_db() as db:
        cur = db.cursor()
        cur.execute(query, tuple(values))
        return cur.fetchall()

