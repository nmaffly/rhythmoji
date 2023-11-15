def generate_avatar_elements(genres):
    avatar_elements = []

    genre_to_elements = {
        'rock': ['leather jacket', 'jeans', 'black shoes', 'sunglasses'],
        'pop': ['colorful outfit', 'g sneakers', 'stylish sunglasses'],
        'hip-hop': ['hoodie', 'baggy pants', 'sneakers', 'cap'],
        'classical': ['elegant dress', 'formal shoes', 'sophisticated glasses'],
        'jazz': ['fedora', 'suit', 'loafers', 'saxophone accessory'],
        'electronic': ['futuristic outfit', 'LED accessories', 'glow sticks'],
        'country': ['cowboy hat', 'denim shirt', 'boots', 'guitar'],
        'reggae': ['rasta hat', 'relaxed outfit', 'sandals', 'dreadlocks'],
        'metal': ['black outfit', 'studded accessories', 'combat boots'],
        'blues': ['vintage shirt', 'hat', 'suede shoes'],
        'folk': ['bohemian outfit', 'wide-brimmed hat', 'ankle boots'],
        'punk': ['punk jacket', 'torn jeans', 'combat boots', 'spiked accessories'],
        'soul': ['stylish suit', 'silk shirt', 'loafers', 'fedora'],
        'funk': ['colorful suit', 'funky glasses', 'platform shoes'],
        'disco': ['glittery outfit', 'bell-bottoms', 'platform shoes'],
        'indie': ['casual shirt', 'chinos', 'sneakers', 'beanie'],
        'r&b': ['stylish jacket', 'fitted jeans', 'sneakers', 'gold jewelry'],
        'techno': ['minimalist outfit', 'sleek sunglasses', 'futuristic shoes'],
        'house': ['casual t-shirt', 'jeans', 'sneakers', 'snapback hat'],
        'trance': ['psychedelic outfit', 'light-up accessories', 'comfortable shoes'],
        # ... Add more genres here
    }

    for genre in genres:
        elements = genre_to_elements.get(genre)
        if elements:
            avatar_elements.extend(elements)

    return list(set(avatar_elements))  # Remove duplicates
