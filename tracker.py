import json
from collections import Counter

LOG_FILE = "app.log"
REPORT_FILE = "report.json"


def read_logs(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()] #dosyada boş satır varsa onları attık elimizde boş olmayan log satırları kaldı
  
def parse_level(line):
    if " ERROR " in line:
        return "ERROR"
    if " WARNING " in line:
        return "WARNING"
    if " INFO " in line:
        return "INFO"
    return "UNKNOWN"


def count_levels(lines):
    levels = [parse_level(line) for line in lines]
    return Counter(levels)
  
def extract_error_message(line):
    # Örnek:
    # 2026-02-11 ... ERROR Database connection failed host=db01
    # Buradan "Database connection failed" kısmını almak istiyoruz.

    if " ERROR " not in line:
        return None

    after_error = line.split(" ERROR ", 1)[1]

    # host=..., module=..., provider=... gibi kısımları keselim
    for token in [" host=", " module=", " provider=", " endpoint=", " ms=", " percent="]:
        if token in after_error:
            after_error = after_error.split(token, 1)[0]

    return after_error.strip()


def most_common_errors(lines, top_n=3):
    errors = []
    for line in lines:
        msg = extract_error_message(line)
        if msg:
            errors.append(msg)

    return Counter(errors).most_common(top_n)


def suggest_fix(error_message):
    msg = error_message.lower()

    if "database connection failed" in msg:
        return "Veritabanı kapalı olabilir veya ağ bağlantısı sorunu olabilir. DB servisini ve bağlantı ayarlarını kontrol et."
    if "timeout" in msg:
        return "Servis yanıt vermiyor olabilir. Network gecikmesi veya API servisinde yoğunluk olabilir."
    if "null pointer" in msg:
        return "Kod içinde None kontrolü eksik olabilir. İlgili modülde değişkenlerin None olup olmadığını kontrol et."
    return "Hata detayını inceleyip ilgili modülü kontrol et."


def build_report(lines):
    level_counts = count_levels(lines)
    top_errors = most_common_errors(lines, top_n=3)

    suggestions = []
    for err, count in top_errors:
        suggestions.append(
            {
                "error": err,
                "count": count,
                "suggestion": suggest_fix(err),
            }
        )

    report = {
        "total_lines": len(lines),
        "levels": dict(level_counts),
        "top_errors": suggestions,
    }

    return report


def save_report(report, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


def main():
    lines = read_logs(LOG_FILE)
    report = build_report(lines)

    print("=== SMART ERROR TRACKER REPORT ===")
    print(f"Total lines: {report['total_lines']}")
    print("Levels:", report["levels"])

    print("\nTop Errors:")
    for item in report["top_errors"]:
        print(f"- {item['error']} (x{item['count']})")
        print(f"  Suggestion: {item['suggestion']}")

    save_report(report, REPORT_FILE)
    print(f"\nReport saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()

