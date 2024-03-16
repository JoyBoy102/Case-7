import uuid
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Экземпляр приложения FastAPI
app = FastAPI(
    title="Case 7 - «Разработка сервиса на Python»"
)


# Модель данных для входного JSON
class Mod(BaseModel):
    array: List


# Словарь для хранения сессий и соответствующих результатов
sessions = {}


def sum_numbers(nums: Mod) -> int:
    """
    Функция для вычисления суммы цифр в списке.

    Args:
        nums (Mod): Модель, содержащая список. Элементами списка могут быть как строки, так и null-значения.

    Returns:
        int: Сумма всех цифр из списка.
    """
    return sum([int(item) for item in nums.array if isinstance(item, str) and item.isdigit()])


@app.post("/")
def sum_array(lst: Mod) -> dict:
    """
    Синхронный метод для вычисления суммы цифр в списке.

    Args:
        lst (Mod): Модель, содержащая список. Элементами списка могут быть как строки, так и null-значения.

    Returns:
        dict: Словарь с результатом вычисления.
    """
    return {"status": 200, "result": sum_numbers(lst)}


@app.post("/async_sum")
async def async_sum(lst: Mod) -> dict:
    """
    Асинхронный метод для вычисления суммы цифр в списке и сохранения результата в словарь сессий.

    Args:
        lst (Mod): Модель, содержащая список. Элементами списка могут быть как строки, так и null-значения.

    Returns:
        dict: Словарь с ID сессии и статусом.
    """
    session_id = str(uuid.uuid4())
    res = sum_array(lst)
    sessions[session_id] = res
    return {"status": 200, "session_id": session_id}


@app.get("/get_sum/{session_id}")
def get_sum(session_id: str) -> dict:
    """
    Метод для получения результата асинхронного вычисления по ID сессии.

    Args:
        session_id (str): ID сессии для получения результата.

    Returns:
        dict: Словарь с результатом вычисления, если сессия найдена в словаре `sessions`.
        В противном случае вызывается исключение HTTPException с кодом состояния 404 и деталями "Session ID not found".
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session ID not found")
    return sessions[session_id]
