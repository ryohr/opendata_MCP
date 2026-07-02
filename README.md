# opendata-mcp

[BODIK オープンデータ](https://data.bodik.jp) (data.bodik.jp) から
日向市（organization: `452068`）のデータセット一覧を取得する MCP サーバーです。

## 提供するツール

| ツール名 | 説明 |
|---|---|
| `get_ckan_datasets` | データセット全件（author・notes・title・groups・resources など）を返す |
| `search_ckan_datasets` | キーワードでデータセットを検索し、上位10件を返す |
| `get_resource_records` | resource_id を指定してリソースのデータ本体（レコード）を取得する |

## 使い方（Claude Desktop）

### 前提

- [uv](https://docs.astral.sh/uv/) がインストールされていること

### 設定

`claude_desktop_config.json` に以下を追加してください。

```json
{
  "mcpServers": {
    "opendata": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/ryohr/opendata_MCP",
        "opendata-mcp"
      ]
    }
  }
}
```

> `<あなたのユーザー名>` を実際の GitHub ユーザー名に置き換えてください。

## ローカルで実行する場合

```bash
git clone https://github.com/ryohr/opendata_MCP
cd opendata_mcp
uv run opendata.py
```
