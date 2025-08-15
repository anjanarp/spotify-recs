# Multilingual Spotify Song Language Classifier and MVP Queue Tool

This project was an attempt to create a personalized listening experience for multilingual listeners. Spotify does not currently offer a way to filter recommendations by language. The goal was to take the songs Spotify recommends for a user and filter them down to only the languages they want to listen to, while still allowing multiple languages for a balanced listening experience.

I used two datasets from Kaggle. One contains a regional breakdown of songs from the Indian subcontinent. The other contains songs that have been popular since the early 1900s. I combined them and used language mapping to produce a labeled dataset for training. The language classification work is in the included notebooks (`data_cleaning.ipynb`, `eda.ipynb`, `classifier.ipynb`) along with the trained model, which you can download from my Google Drive:

https://drive.google.com/drive/folders/1TnGHmxL3nCAzTSATZOpzdhNeOENY73GA?usp=drive_link

The model takes Spotify numeric audio features, track-level embeddings, and artist-level embeddings and predicts the language of a track. It uses a Random Forest classifier trained on the combined dataset after filtering out languages with too few samples.

Originally, the plan was to integrate this with Spotify's recommendation endpoints so it could pull new recommended songs for a user, classify them, filter them by the selected languages, and continuously queue them for playback. Spotify has since deprecated the key endpoints that made this possible in real time, so that part of the project is on hold.

As a workaround, I wrote another script (`mvp.py`) that can append either an artist's (well I can choose to do so for one artists or many artists) entire discography or specific albums to one large list, sort it by popularity scores, and push it to your Spotify queue. This still gives a way to find new music in a semi-automated way, even though it is not filtered by language.

To run `mvp.py` you need a Spotify Developer account. Create an app in the Spotify Developer Dashboard to get a client ID and client secret, set a redirect URI (such as `http://localhost:8080`), and export them along with your Spotify username as environment variables before running the script.
