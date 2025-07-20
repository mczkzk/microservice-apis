# 非同期
# from ariadne.asgi import GraphQL

# from web.schema import schema

# server = GraphQL(schema, debug=True)


from ariadne import make_executable_schema, QueryType
from ariadne.asgi import GraphQL

schema = """
type Query {
    hello: String
}
"""

# QueryTypeのインスタンスを作成
query = QueryType()


# field()デコレータでリゾルバをバインド
@query.field("hello")
def resolve_hello(*_):
    return "Hello, GraphQL!"


# make_executable_schemaにバインド可能オブジェクトを配列として渡す
server = GraphQL(make_executable_schema(schema, [query]), debug=True)


# def simple_resolver(obj: Any, info: GraphQLResolveInfo):
#     pass
