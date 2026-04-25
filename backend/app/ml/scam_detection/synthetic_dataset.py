from app.schemas.scam_detection import ScamTrainingExample


SCAM_TRAINING_EXAMPLES: list[ScamTrainingExample] = [
    ScamTrainingExample(
        text="Guaranteed profit if you invest today. This opportunity has no risk and you cannot lose.",
        label="scam",
    ),
    ScamTrainingExample(
        text="Double your money in 7 days with this new crypto project. Join now before it is too late.",
        label="scam",
    ),
    ScamTrainingExample(
        text="Send your wallet address to claim exclusive early access to a guaranteed return token.",
        label="scam",
    ),
    ScamTrainingExample(
        text="This viral token is the next Bitcoin. Everyone is buying and profits are guaranteed.",
        label="scam",
    ),
    ScamTrainingExample(
        text="Act now for 20% daily profit. Limited time opportunity only available through our Telegram group.",
        label="scam",
    ),
    ScamTrainingExample(
        text="Celebrity backed crypto launch with huge returns. DM me privately to secure your allocation.",
        label="scam",
    ),
    ScamTrainingExample(
        text="Risk free investment plan with massive returns every week. Only today for new members.",
        label="scam",
    ),
    ScamTrainingExample(
        text="Join our private WhatsApp group and send funds now to access the presale before public launch.",
        label="scam",
    ),
    ScamTrainingExample(
        text="This project describes tokenised assets and explains that returns are uncertain and market values can fall.",
        label="safe",
    ),
    ScamTrainingExample(
        text="The investment material explains volatility, diversification, fees, and the possibility of losing money.",
        label="safe",
    ),
    ScamTrainingExample(
        text="This educational article compares different asset classes and warns that past performance does not guarantee future returns.",
        label="safe",
    ),
    ScamTrainingExample(
        text="The platform provides a simulated portfolio scenario for learning purposes and does not provide financial advice.",
        label="safe",
    ),
    ScamTrainingExample(
        text="The document explains that cryptocurrency markets are volatile and users should research projects carefully.",
        label="safe",
    ),
    ScamTrainingExample(
        text="This guide introduces long-term investing concepts, risk tolerance, portfolio diversification, and scam awareness.",
        label="safe",
    ),
    ScamTrainingExample(
        text="The asset description includes clear risk warnings, transparent fees, and no promises of guaranteed profit.",
        label="safe",
    ),
    ScamTrainingExample(
        text="The learning material explains how market uncertainty affects portfolio outcomes and why users should avoid hype.",
        label="safe",
    ),
    ScamTrainingExample(
        text="This token has strong community hype and could rise quickly, but users should research the risks carefully.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="The project claims high returns but also says users should understand volatility before participating.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="Early access is available for a limited period, although the project documentation includes some risk warnings.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="The advert promotes large growth potential and encourages quick action, but does not explicitly guarantee returns.",
        label="suspicious",
    ),

        ScamTrainingExample(
        text="Our investment platform explains that crypto prices can be volatile and that users may lose money.",
        label="safe",
    ),
    ScamTrainingExample(
        text="This learning resource explains how diversification can reduce concentration risk but cannot remove market risk.",
        label="safe",
    ),
    ScamTrainingExample(
        text="The project documentation includes transparent fees, risk warnings, team information, and no guaranteed returns.",
        label="safe",
    ),
    ScamTrainingExample(
        text="This educational simulator allows users to compare portfolio outcomes without making real trades.",
        label="safe",
    ),
    ScamTrainingExample(
        text="The article explains stablecoins, tokenised assets, volatility, regulation, and the importance of independent research.",
        label="safe",
    ),
    ScamTrainingExample(
        text="This guide warns beginners to avoid social media hype and to check whether investment claims are realistic.",
        label="safe",
    ),
    ScamTrainingExample(
        text="This digital asset overview describes possible growth but clearly states that returns are uncertain.",
        label="safe",
    ),
    ScamTrainingExample(
        text="The investment summary encourages users to read the risk disclosure before considering any asset.",
        label="safe",
    ),
    ScamTrainingExample(
        text="Early access investors may receive large gains if demand increases, but the outcome is not guaranteed.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="The token is being heavily promoted online and supporters claim it could become very valuable quickly.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="This asset has strong community momentum, although the project has limited independent verification.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="The project encourages users to join quickly before public launch, but provides only limited technical details.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="The message mentions high growth potential and early access but does not clearly explain downside risks.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="The promoter says many people are already buying, but there is little independent evidence available.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="The asset description suggests fast growth and exclusive access, while giving limited information about fees.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="The project uses social media hype to attract attention but provides only basic documentation.",
        label="suspicious",
    ),
    ScamTrainingExample(
        text="Guaranteed 50% weekly profit for every investor. Deposit now to secure your position.",
        label="scam",
    ),
    ScamTrainingExample(
        text="No risk crypto investment with fixed daily returns. Send funds today before registration closes.",
        label="scam",
    ),
    ScamTrainingExample(
        text="You cannot lose with this private token sale. Message me privately and send your wallet address.",
        label="scam",
    ),
    ScamTrainingExample(
        text="Last chance to double your money. Our Telegram group gives guaranteed winning trades.",
        label="scam",
    ),
    ScamTrainingExample(
        text="Risk free digital asset opportunity offering massive daily profit to all early members.",
        label="scam",
    ),
    ScamTrainingExample(
        text="Celebrity approved token with guaranteed returns. Only selected investors can join through WhatsApp.",
        label="scam",
    ),
    ScamTrainingExample(
        text="Send crypto today and receive double tomorrow. Limited slots available for serious investors.",
        label="scam",
    ),
    ScamTrainingExample(
        text="This investment cannot fail and all members receive fixed profits every day.",
        label="scam",
    ),
]


def get_scam_training_examples() -> list[ScamTrainingExample]:
    return SCAM_TRAINING_EXAMPLES


def get_training_texts_and_labels() -> tuple[list[str], list[str]]:
    examples = get_scam_training_examples()

    texts = [example.text for example in examples]
    labels = [example.label for example in examples]

    return texts, labels