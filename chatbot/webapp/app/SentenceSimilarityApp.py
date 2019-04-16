from SentenceSimilarity import SentenceSimilarityHandler

messages = [
                # "Application software is, essentially, software that allows the user to accomplish some goal or purpose. For example, if you have to write a paper, you might use the application-software program Microsoft Word.",
                # "An application is any program, or group of programs, that is designed for the end user. Applications software (also called end-user programs) include such things as database programs, word processors, Web browsers and spreadsheets.",
                "It possible",
                "It is not possible"
        ]
similarityValue = SentenceSimilarityHandler.validate(messages)
print("Similarity value is", similarityValue)
