import openai


def query_gpt(query):

    user_1 = 'I want you to act as a playlist generator.I will provide short descriptions of music, and you will ' \
             'suggest a names for the playlists and lists of songs that fit the description. '
    assistant_1 = 'OK'
    user_2 = 'Songs from the 90s, UK, upbeat, not in the charts'
    assistant_2 = ('90s Britpop Bangers:\n'
                   '1. You\'re Gorgeous - Babybird\n'
                   '2. The Only One I Know - The Charlatans\n'
                   '3. Born Slippy - Underworld\n'
                   '4. Bittersweet Symphony - The Verve\n'
                   '5. Step On - Happy Mondays\n'
                   '6. Sit Down - James\n'
                   '7. Common People - Pulp\n'
                   '8. Love is the Law - The Seahorses\n'
                   '9. Roll With It - Oasis\n'
                   '10. One to Another - The Charlatans')

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_1},
            {"role": "assistant", "content": assistant_1},
            {"role": "user", "content": user_2},
            {"role": "assistant", "content": assistant_2},
            {"role": "user", "content": query}
        ]
    )

    playlist = response["choices"][0]["message"]["content"]
    print("GPT response received ...\n'{}'".format(playlist))
    return playlist.partition("\n\n")[2].replace('\n', ', ')


def test_query_gpt():
    query = "Songs from the 90s, UK, upbeat."
    return query_gpt(query)
