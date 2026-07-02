import requests
from fastmcp import FastMCP

app = FastMCP("CKAN Dataset Server")

CKAN_BASE = "https://data.bodik.jp/api/3/action/package_search"
ORGANIZATION = "452068"  # 固定


def extract_datasets(results: list) -> list:
    """results配列からデータセット情報を抽出する共通関数"""
    datasets = []

    for dataset in results:
        resources = []
        for r in dataset.get("resources", []):
            resources.append({
                "id": r.get("id"),
                "name": r.get("name"),
                "format": r.get("format"),
                "url": r.get("url"),
            })

        datasets.append({
            "author": dataset.get("author"),
            "metadata_created": dataset.get("metadata_created"),
            "metadata_modified": dataset.get("metadata_modified"),
            "notes": dataset.get("notes"),
            "title": dataset.get("title"),
            "groups": [g.get("title") for g in dataset.get("groups", [])],
            "resources": resources,
        })

    return datasets


@app.tool()
def get_ckan_datasets() -> dict:
    """
    organization=452068 の CKAN データセット全件一覧を返す。
    各データセットの resource.name と resource.id を含む。
    「データセット一覧を見せて」など、全件取得が必要な場合に使用する。
    """
    # Step1: rows=0 で総件数だけ取得
    count_url = f"{CKAN_BASE}?fq=organization:{ORGANIZATION}&rows=0"
    count_response = requests.get(count_url)
    count_response.raise_for_status()
    total = count_response.json()["result"]["count"]

    # Step2: 1000件ずつページネーションして全件取得
    PAGE_SIZE = 1000
    all_results = []

    for start in range(0, total, PAGE_SIZE):
        url = f"{CKAN_BASE}?fq=organization:{ORGANIZATION}&rows={PAGE_SIZE}&start={start}"
        response = requests.get(url)
        response.raise_for_status()
        all_results.extend(response.json()["result"]["results"])

    datasets = extract_datasets(all_results)

    return {
        "count": len(datasets),
        "datasets": datasets
    }


@app.tool()
def search_ckan_datasets(keyword: str) -> dict:
    """
    organization=452068 の CKAN データセットをキーワードで検索し、
    上位10件を返す。特定のデータセットを探す場合に使用する。
    """
    url = f"{CKAN_BASE}?fq=organization:{ORGANIZATION}&q={keyword}&rows=10"

    response = requests.get(url)
    response.raise_for_status()

    results = response.json()["result"]["results"]
    datasets = extract_datasets(results)

    return {
        "count": len(datasets),
        "keyword": keyword,
        "datasets": datasets
    }


CKAN_DATASTORE_SEARCH = "https://data.bodik.jp/api/3/action/datastore_search"


@app.tool()
def get_resource_records(resource_id: str) -> dict:
    """
    resource_id を直接受け取り、
    datastore_search でデータの中身を取得して返す。
    resource_idはget_ckan_datasetsまたはsearch_ckan_datasetsで取得したid
    """

    url = f"{CKAN_DATASTORE_SEARCH}?resource_id={resource_id}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    return {
        "resource_id": resource_id,
        "records": data["result"]["records"]
    }


if __name__ == "__main__":
    app.run()