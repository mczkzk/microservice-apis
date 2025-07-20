# 非同期
from ariadne.asgi import GraphQL

from web.schema import schema

server = GraphQL(schema, debug=True)
