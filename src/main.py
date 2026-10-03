from contextlib import asynccontextmanager

import strawberry
from fastapi import FastAPI, APIRouter
from starlette.staticfiles import StaticFiles
from strawberry.fastapi import GraphQLRouter

from src.api.graphql.resolvers import Query, Mutation
from src.api.rest.product.views import products_router
from src.api.rest.user.views import users_router
from src.dependencies import context_dependency
from src.infrastructure.database.base import engine, Base



app = FastAPI()

api_v1_router = APIRouter(prefix="/v1/api")
api_v1_router.include_router(products_router)
api_v1_router.include_router(users_router)
app.include_router(api_v1_router)


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=context_dependency, multipart_uploads_enabled=True)

app.include_router(graphql_app, prefix="/v1/graphql")
#app.mount("/media", StaticFiles(directory="media"), name="media")