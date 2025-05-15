import requests
import base64
from const import BACK_URL
from utils import format_name


def test_api(file_name: str) -> None:
    with open(file_name, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode('utf-8')
    res = requests.post(BACK_URL, json={"file": encoded_file})

    if res.status_code == 200:
        decoded_content = base64.b64decode(res.json()["file"])
        with open(format_name(file_name), "wb") as f:
            f.write(decoded_content)
            print(f"Archivo '{format_name(file_name)}' convertido a PDF")
            return

    print(f"Error convertirtiendo el archivo '{format_name(file_name)}'")
    return


if __name__ == "__main__":
    test_api("pdf.png")
