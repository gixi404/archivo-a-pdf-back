import requests
from const import BACK_URL
from utils import format_name


def test_api(file_name: str) -> None:
    file = {"file": open(file_name, "rb")}
    res = requests.post(BACK_URL, files=file)

    if res.status_code == 200:
        with open(format_name(file_name), "wb") as f:
            f.write(res.content)
            print(f"Archivo '{format_name(file_name)}' convertido PDF")
            return

    print(f"Error convertirtiendo el archivo '{format_name(file_name)}'")
    return


if __name__ == "__main__":
    test_api("sin titulo.png")
