import re


def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)


def find_pattern(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0).strip() if match else "Not found"


def find_in_sentences(pattern, sentences):
    for sentence in sentences:
        if re.search(pattern, sentence, re.IGNORECASE):
            return sentence.strip()
    return "Not found"


def extract_sla(text: str):

    sentences = split_sentences(text)

    data = {
        "interest_rate": find_pattern(
            r"\d+(\.\d+)?\s*%.*?(APR|interest rate)", text
        ),

        "lease_term": find_pattern(
            r"(contract duration|term).*?\d+\s*(months?|years?)", text
        ),

        "monthly_payment": find_pattern(
            r"(₹|\$)\s?\d{1,3}(,\d{3})*(\.\d+)?\s*(per month|/month|monthly)", text
        ),

        "down_payment": find_pattern(
            r"down payment.*?(₹|\$)\s?\d{1,3}(,\d{3})*", text
        ),

        "residual_value": find_pattern(
            r"residual value.*?(₹|\$)\s?\d{1,3}(,\d{3})*", text
        ),

        "mileage_limit": find_in_sentences(
            r"(km|kilometers|miles)", sentences
        ),

        "buyout_price": find_pattern(
            r"buyout price.*?(₹|\$)\s?\d{1,3}(,\d{3})*", text
        ),

        "maintenance": find_in_sentences(
            r"(maintenance|servicing|repair)", sentences
        ),

        "warranty": find_pattern(
            r"\d+\s*(year|years).*warranty", text
        ),

        "penalties": find_in_sentences(
            r"(penalty|fine|late fee)", sentences
        ),
    }

    return data


def detect_risks(text: str):
    risks = []
    text_lower = text.lower()

    risk_patterns = {
        "Penalty clause detected": r"\bpenalt(y|ies)\b",
        "Early termination clause present": r"\btermination\b",
        "Late fee charges mentioned": r"\blate fee\b",
        "Non-refundable charges present": r"\bnon[- ]?refundable\b",
        "Additional hidden charges possible": r"\badditional charges\b",
        "Liability clause present": r"\bliability\b",
        "Breach clause present": r"\bbreach\b"
    }

    for message, pattern in risk_patterns.items():
        if re.search(pattern, text_lower):
            risks.append(message)

    return risks


def fairness_score(risks):
    weights = {
        "Penalty clause detected": 15,
        "Early termination clause present": 12,
        "Late fee charges mentioned": 10,
        "Non-refundable charges present": 10,
        "Additional hidden charges possible": 8,
        "Liability clause present": 8,
        "Breach clause present": 8
    }

    score = 100
    for risk in risks:
        score -= weights.get(risk, 8)

    return max(score, 50)
