from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.endpoints import citas

from app.models.models import Paciente, Medico, Cita

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(citas.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)