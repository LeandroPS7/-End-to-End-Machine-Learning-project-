# Filmrating Prediction

## Project Description  
Predicts the average audience rating (1–5 stars) of a movie based on metadata like budget, runtime, release year, genre and production studio.
Final model is deployed as a Gradio app on Hugging Face.

---

## Results  
The final model achieves a **Test RMSE of 0.95** — despite excluding user voting data.  
This makes it suitable for early-stage rating predictions.  
Feature importance is more evenly distributed after removing `vote_average`, with `release_year`, `runtime`, and `budget` emerging as most influential.

---

## Name & URL

| Name           | URL                                                                 |
|----------------|----------------------------------------------------------------------|
| Huggingface    | [Huggingface Space](https://huggingface.co/spaces/pereilea/movie_rating_guesser) |
| Code           | [GitHub Repository](https://github.com/LeandroPS7/-End-to-End-Machine-Learning-project-) |

---

## Data Sources and Features Used Per Source

| Data Source                                                                                  | Features Used                                                              |
|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| [TMDB Movie Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)              | `budget`, `runtime`, `release_date`, `title`, `genres`, `production_companies`, `vote_average`, `vote_count` |
| [MovieLens 20M Dataset](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset)     | `movieId`, `tmdbId`, `rating` (used as target), `userId`, `timestamp` *(linked via tmdbId)* |


## Features Created

| Feature               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `release_year`        | Extracted from `release_date`                                               |
| `title_length`        | Character length of movie title                                             |
| `vote_ratio`          | `vote_average * vote_count` (used in earlier iterations only)              |
| `top_genre_X`         | One-hot encoding of top 10 most common genres                               |
| `top_studio_X`        | One-hot encoding of top 10 most common studios                              |

---

## Model Training

### Amount of Data  
~100,000 movies in raw dataset  
~70,000 after filtering and removing missing values

### Data Splitting Method (Train/Validation/Test)  
Initial 80/20 split → Cross-validation used during GridSearch (3-fold)

---

## Performance

| It. Nr | Model             | Performance                             | Features                            | Description                           |
|--------|-------------------|------------------------------------------|-------------------------------------|----------------------------------------|
| 1      | Linear Regression | Train RMSE: 0.96, Test RMSE: 1.01        | budget, runtime, vote_average       | Baseline                              |
| 2      | Random Forest     | Train RMSE: 0.63, Test RMSE: 0.99        | Same as It. 1                       | Overfitting                           |
| 3      | Random Forest     | Test RMSE: 0.98                          | budget, runtime, release_year, title_length, vote_ratio | New features added |
| 4      | Random Forest     | Test RMSE: 0.96                          | budget, runtime, vote_average       | Vote average re-tested                |
| 5      | Random Forest     | Test RMSE: 0.95                          | + top 10 genres + top 10 studios    | Feature expansion                     |
| 6      | Random Forest     | Test RMSE: 0.95                          | Without vote_average                | Better generalization                 |
| 7      | GridSearch RF     | Test RMSE: 0.95                          | Same as It. 6                       | Optimized hyperparameters             |
| 8      | Final RF Model    | Test RMSE: 0.95                          | Same as It. 7                       | Used for Hugging Face deployment      |

---

## References  
**Top 5 Feature Importances (Final Model):**

- `release_year`
- `runtime`
- `budget`
- `top_genre_Drama`
- `top_studio_Warner Bros.`

