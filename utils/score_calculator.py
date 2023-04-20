LIKE_WEIGHT = 1
COMMENT_WEIGHT = 5
RETWEET_WEIGHT = 20

# bonus in percentage
TEN_BONUS = 20
HUNDRED_BONUS = 35
THOUSAND_BONUS = 50


def calculate_score(likes: int, comments: int, retweets: int) -> int:
    """
    Calculate a score based on likes, comments, and retweets
    :param likes: number of likes
    :param comments: number of comments
    :param retweets: number of retweets
    :return: score
    """
    return (
        calculate(likes, LIKE_WEIGHT)
        + calculate(comments, COMMENT_WEIGHT)
        + calculate(retweets, RETWEET_WEIGHT)
    )


def calculate(count: int, weight: int) -> int:
    """
    Calculate a score based on a count and weight
    :param count: count
    :param weight: weight
    :return: score
    """
    score = count * weight
    ten_count = score // 10
    hundred_count = score // 100
    thousand_count = score // 1000
    score += 10 * weight * ten_count * TEN_BONUS / 100
    score += 100 * weight * hundred_count * HUNDRED_BONUS / 100
    score += 1000 * weight * thousand_count * THOUSAND_BONUS / 100
    return round(score)
