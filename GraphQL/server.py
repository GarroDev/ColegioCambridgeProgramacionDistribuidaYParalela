import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from GraphQL.schema import schema

app = FastAPI(title="Colegio Cambridge - GraphQL API")

graphql_app = GraphQLRouter(schema, graphiql=True)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def root():
    return {"status": "ok", "service": "graphql"}
