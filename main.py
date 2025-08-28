from fastapi import FastAPI, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

app = FastAPI() # fastapi를 사용해서 서버 만들기

@app.post('/items')
async def create_items(image:UploadFile, # 각 함수로부터 받을 것들: 타입
                 title:Annotated[str,Form()],
                 price:Annotated[int,Form()],
                 description:Annotated[str,Form()], 
                 place:Annotated[str,Form()],
                 insertAt: Annotated[int, Form()]
                 ):
    image_bytes = await image.read() # 이미지 읽을 시간 확보
    # 데이터베이스에 가져온 정보들 insert하기
    cur.execute(f"""
                INSERT INTO items(title, image, price, description, place, insertAt)
                VALUES ('{title}', '{image_bytes.hex()}', {price}, '{description}', '{place}', {insertAt})
                """)
    con.commit()
    return '200'

@app.get('/items')
async def get_items():
    # 컬럼명도 가져와서 dictionary에 사용
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                        SELECT * from items;
                        """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

