from fastapi import FastAPI
from pathlib import Path
import yaml

# マイクロサービス
app = FastAPI(debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders")

# API ドキュメントを読み込む
oas_doc = yaml.safe_load((Path(__file__).parent / "oas.yaml").read_text())

# FastAPI の OpenAPI ドキュメントを上書きする
app.openapi = lambda: oas_doc

from orders.api import api
