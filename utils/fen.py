import re

def is_fen_syntax_valid(fen: str) -> bool:
        # Code for this function taken from: https://gist.github.com/Dani4kor/e1e8b439115878f8c6dcf127a4ed5d3e
        # Some small changes have been made to the code.

        regexMatch = re.match(
            r"\s*^(((?:[rnbqkpRNBQKP1-8]+\/){7})[rnbqkpRNBQKP1-8]+)\s([b|w])\s(-|[K|Q|k|q]{1,4})\s(-|[a-h][1-8])\s(\d+\s\d+)$",
            fen,
        )
        if not regexMatch:
            return False
        regexList = regexMatch.groups()
        if len(regexList[0].split("/")) != 8:
            return False  # 8 rows not present.
        for fenPart in regexList[0].split("/"):
            field_sum = 0
            previous_was_digit = False
            for c in fenPart:
                if c in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                    if previous_was_digit:
                        return False  # Two digits next to each other.
                    field_sum += int(c)
                    previous_was_digit = True
                elif c.lower() in ["p", "n", "b", "r", "q", "k"]:
                    field_sum += 1
                    previous_was_digit = False
                else:
                    return False  # Invalid character.
            if field_sum != 8:
                return False  # One of the rows doesn't have 8 columns.
        return True