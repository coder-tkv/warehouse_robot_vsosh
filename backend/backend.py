import uvicorn
from logics import logics_main
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/auto')
async def auto_mode(bg_tasks: BackgroundTasks):
    bg_tasks.add_task(logics_main.run, True, None, None)
    return {'ok': True}


@app.post('/manual')
async def manual_mode(x: int, y: int, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(logics_main.run, False, x, y)
    return {'ok': True}


@app.get('/position')
async def get_pos():
    coords = logics_main.get_robot_pos()
    if coords is None:
        raise HTTPException(status_code=500, detail='Робот не найден')
    return {'x': coords[0], 'y': coords[1]}


if __name__ == '__main__':
    uvicorn.run('backend:app', host='0.0.0.0')
