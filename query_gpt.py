import openai


def query_gpt(query):
    print(openai.api_key)
    prefix = "Please provide a list of songs that can be described as: "
    postfix = " Please list them in the format: Song title - Artist"

    content = prefix + query + postfix
    print(content)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
    )

    playlist = response["choices"][0]["message"]["content"]
    print(playlist)
    return playlist.partition("\n\n")[2].replace('\n', ', ')


def test_query_gpt():
    query = "Songs from the 90s, UK, upbeat."
    return query_gpt(query)
