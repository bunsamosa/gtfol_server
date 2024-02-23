URL_REGEX = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
AMPERSAND_CHARS = {"&amp;amp;": "&", "&amp;": "&", "&gt;": ">", "&lt": "<"}
AMPERSAND_REGEX = r"&(\w){2,};"
