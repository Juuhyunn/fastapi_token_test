import uvicorn
from fastapi import FastAPI


def create_app():
    """
    앱 함수 실행
    :return:
    """
    app = FastAPI()

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("user:app", host="localhost", port=8080, reload=True)