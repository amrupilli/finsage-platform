from pydantic import BaseModel


class InvestmentChecklistItem(BaseModel):
    title: str
    status: str
    explanation: str


class InvestmentCheckResponse(BaseModel):
    input_text: str
    risk_level: str
    summary: str
    checklist: list[InvestmentChecklistItem]
    educational_message: str


def assess_investment_question(input_text: str) -> InvestmentCheckResponse:
    text = input_text.lower()

    high_risk_assets = [
        "crypto",
        "bitcoin",
        "btc",
        "ethereum",
        "eth",
        "xrp",
        "ripple",
        "dogecoin",
        "meme coin",
        "nft",
        "forex",
        "penny stock",
        "options",
        "leverage",
        "margin",
    ]

    medium_risk_assets = [
        "stock",
        "shares",
        "equity",
        "fund",
        "etf",
        "index fund",
        "mutual fund",
    ]

    lower_risk_assets = [
        "cash isa",
        "savings",
        "government bond",
        "treasury",
        "fixed deposit",
        "premium bonds",
    ]

    scam_warning_terms = [
        "guaranteed",
        "no risk",
        "double your money",
        "quick profit",
        "urgent",
        "limited time",
        "secret",
        "insider",
        "telegram",
        "whatsapp",
        "send money",
        "will definitely go up",
        "guaranteed profit",
    ]

    matched_high_risk = [term for term in high_risk_assets if term in text]
    matched_medium_risk = [term for term in medium_risk_assets if term in text]
    matched_low_risk = [term for term in lower_risk_assets if term in text]
    matched_scam_terms = [term for term in scam_warning_terms if term in text]

    if matched_scam_terms:
        risk_level = "High risk"
        summary = (
            "This opportunity contains strong warning signs such as guaranteed returns, urgency, or unrealistic claims. "
            "A beginner should be very cautious and should not rely on social media claims alone."
        )
    elif matched_high_risk:
        risk_level = "High risk"
        summary = (
            "This appears to involve a high-risk asset class. Crypto, leveraged products, meme coins, NFTs, forex, "
            "and penny stocks can move sharply up or down, so they may not be suitable for beginners without further research."
        )
    elif matched_low_risk:
        risk_level = "Low risk"
        summary = (
            "This appears to involve a lower-risk savings or government-backed type of product. It may still have limits, "
            "fees, inflation risk, or access restrictions, so the details should still be checked."
        )
    elif matched_medium_risk:
        risk_level = "Medium risk"
        summary = (
            "This appears to involve a mainstream investment such as stocks, funds, or ETFs. These can grow over time, "
            "but their value can still fall, especially in the short term."
        )
    else:
        risk_level = "Unknown risk"
        summary = (
            "FinSage cannot clearly identify the asset type from this description. The user should check what the investment is, "
            "how it makes money, what could go wrong, and whether the provider is trustworthy."
        )

    checklist = [
        InvestmentChecklistItem(
            title="What exactly am I investing in?",
            status="Essential",
            explanation=(
                "Identify the asset clearly. Is it crypto, a stock, a fund, a bond, a savings product, or something else? "
                "Beginners should not invest in something they cannot explain in simple words."
            ),
        ),
        InvestmentChecklistItem(
            title="How risky is this asset type?",
            status="Essential",
            explanation=(
                "Check whether the asset is normally low, medium, or high risk. Crypto, penny stocks, leverage, and forex "
                "are usually much riskier than diversified funds or savings products."
            ),
        ),
        InvestmentChecklistItem(
            title="Could I lose money?",
            status="Essential",
            explanation=(
                "Ask how much money could realistically be lost. If the answer is unclear, or someone says there is no risk, "
                "that is a warning sign."
            ),
        ),
        InvestmentChecklistItem(
            title="Why do people think it will go up?",
            status="Check evidence",
            explanation=(
                "Do not rely only on hype, TikTok, Telegram, Reddit, or friends. Look for clear evidence such as business performance, "
                "adoption, regulation, market conditions, or fund details."
            ),
        ),
        InvestmentChecklistItem(
            title="Who is behind it?",
            status="Check credibility",
            explanation=(
                "Check whether the platform, company, project team, or provider is real, transparent, and regulated where relevant."
            ),
        ),
        InvestmentChecklistItem(
            title="Can I exit easily?",
            status="Check liquidity",
            explanation=(
                "Check whether you can sell or withdraw easily. Some investments have lock-ins, high fees, withdrawal limits, "
                "or poor liquidity."
            ),
        ),
        InvestmentChecklistItem(
            title="Are there scam warning signs?",
            status="Warning check",
            explanation=(
                "Be careful with guaranteed profits, pressure to act quickly, private messages, secret tips, or requests to transfer money directly."
            ),
        ),
    ]

    return InvestmentCheckResponse(
        input_text=input_text,
        risk_level=risk_level,
        summary=summary,
        checklist=checklist,
        educational_message=(
            "This is an educational risk check, not financial advice. FinSage does not tell users whether to buy or avoid an investment. "
            "It helps beginners understand what to check before making a decision."
        ),
    )