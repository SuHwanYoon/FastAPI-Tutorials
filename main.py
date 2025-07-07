from fastapi import FastAPI, Query , HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic 모델을 정의합니다.
# Pydantic은 데이터 유효성 검사와 설정 관리를 위한 라이브러리입니다.
# 이 모델은 아이템의 텍스트와 완료 여부를 나타냅니다.
# text는 문자열이며, is_done은 불리언 값으로 기본값은 False입니다
class Item(BaseModel):
    text: str
    is_done: bool = False
 
# 전역 변수로 items 리스트를 선언합니다.
# 이 리스트는 문자열을 저장하는 용도로 사용됩니다.
items = []


@app.get("/")
def root():
    return {"message": "Hello, World!"}

#  post리퀘스트를 처리하는 엔드포인트
#  이 엔드포인트는 문자열을 받아서 items 리스트에 추가합니다.
#  반환값은 추가된 문자열입니다.
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items")
def list_items(skip: int = 0, limit: int = 10) -> list:
    """
    아이템 목록을 조회하는 엔드포인트입니다.
    skip과 limit 파라미터를 사용하여 아이템을 페이징 처리합니다.
    """
    return items[skip: skip + limit]


@app.get("/items/{item_id}")
def read_item(item_id: int) -> Item:
    """
    특정 아이템을 조회하는 엔드포인트입니다.
    아이템 ID에 해당하는 문자열을 반환합니다.
    """
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return items[item_id]