import requests


def test_api():
    url = "http://127.0.0.1:5000/convert_png"
    file = {"file": open("homero.png", "rb")}
    res = requests.post(url, files=file)

    if res.status_code == 200:
        with open("resultado.pdf", "wb") as f:
            f.write(res.content)
        print("PDF guardado como resultado.pdf")
    else:
        print("Error al convertir: ", res.json())


if __name__ == "__main__":
    test_api()
