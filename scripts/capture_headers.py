import requests
import os

def save_headers(url, output_filename):
    response = requests.get(url)
    output_path = os.path.join("evidence", output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Status Code: {response.status_code}\n")
        for key, value in response.headers.items():
            f.write(f"{key}: {value}\n")

    print(f"Headers saved to {output_path}")

if __name__ == "__main__":
    save_headers("http://127.0.0.1:5000/", "headers_after.txt")