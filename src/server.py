"""AppBLX"""
#-----------------------
# BIBLIOTECAS
#-----------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import router_exemplo, router_rastreio
#-----------------------
# FastApi
#-----------------------
app = FastAPI();
#-----------------------
# CORS
#-----------------------
origins = [
    "http://localhost",
    "http://localhost:8000",
];

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
);
#-----------------------
# Routers
#-----------------------
app.include_router(router_exemplo.router);
app.include_router(router_rastreio.router);
#-----------------------