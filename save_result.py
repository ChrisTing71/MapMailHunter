import json

def save_results(data, filename="results.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"結果已儲存到 {filename}")
