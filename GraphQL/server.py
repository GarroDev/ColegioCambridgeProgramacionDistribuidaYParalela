import sys, os
# permitir imports relativos al ejecutar desde raíz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from GraphQL.schema import schema

# Crea app FastAPI y monta /graphql
app = FastAPI(title="Colegio Cambridge - GraphQL API")
graphql_app = GraphQLRouter(schema, graphiql=True)
app.include_router(graphql_app, prefix="/graphql")

# Estado simple (opcional)
@app.get("/")
def root():
    return {"status": "ok", "service": "graphql"}

# Ejecutable con: uvicorn GraphQL.server:app --reload
