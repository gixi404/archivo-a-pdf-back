from flask import jsonify
import requests
from const import BACK_URL


def test_api(file_name: str) -> None:
    file = {"file": open(file_name, "rb")}
    res = requests.post(BACK_URL, files=file)

    if res.status_code == 200:
        with open(format_name(file_name), "wb").write(res.content):
            return jsonify({
                "message": f"Archivo {format_name(file_name)} convertido PDF"
                }), 200

    return jsonify({
         "error": f"Error convertirtiendo el archivo {format_name(file_name)}"
         }), 200


def format_name(name: str) -> str:
    name = name.lower().replace(" ", "-").replace(".png", "")
    return name if name.endswith(".pdf") else name + ".pdf"


if __name__ == "__main__":
    test_api("arboleada.png")
