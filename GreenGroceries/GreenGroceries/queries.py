from GreenGroceries import db_cursor


def get_words_by_filters(word=None, language=None, category=None, country=None):
    sql = """
    SELECT w.word_id, w.word, l.language, c.category, co.country
    FROM Word w
    JOIN Has h ON h.word_id = w.word_id
    JOIN Language l ON l.language_id = h.language_id
    LEFT JOIN BelongsTo bt ON bt.word_id = w.word_id
    LEFT JOIN Category c ON c.category_id = bt.category_id
    LEFT JOIN Speaks s ON s.language_id = l.language_id
    LEFT JOIN Country co ON co.country_id = s.country_id
    WHERE 1=1
    """
    conditionals = []
    if word:
        conditionals.append(f"w.word ILIKE '%{word}%'")
    if language:
        conditionals.append(f"l.language ILIKE '{language}'")
    if category:
        conditionals.append(f"c.category ILIKE '{category}'")
    if country:
        conditionals.append(f"co.country ILIKE '{country}'")

    if conditionals:
        sql += " AND " + " AND ".join(conditionals)

    sql += " ORDER BY w.word_id"
    db_cursor.execute(sql)
    words = [dict(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return words
