import requests
from fastmcp import FastMCP

app = FastMCP("CKAN Dataset Server")

CKAN_BASE = "https://data.bodik.jp/api/3/action/package_search"
ORGANIZATION = "452068"  # 日向市


@app.tool()
def get_ckan_datasets() -> dict:
    """
    organization=452068 の CKAN データセット一覧を、
    title と package_id（id）だけ返す。
    """
    url = f"{CKAN_BASE}?q=organization:{ORGANIZATION}"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    results = data["result"]["results"]

    datasets = [
        {
            "title": d["title"],
            "package_id": d["id"]
        }
        for d in results
    ]

    return {
        "count": len(datasets),
        "datasets": datasets
    }


def serve():
    app.run()


if __name__ == "__main__":
    serve()
