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
200,000 movies 

### Data Splitting Method (Train/Validation/Test)  
**Train/Test Split:** 80/20
****Cross-Validation:** 5-fold CV for iterations 1–5, GridSearch in iteration 7

---

## 📈 Performance Table

| Iteration | Model(s)             | RMSE (CV/Train/Test)          | Features Summary                             | Hypothesis                                               | Result                                                       |
|-----------|----------------------|-------------------------------|----------------------------------------------|-----------------------------------------------------------|--------------------------------------------------------------|
| 1         | Linear Regression, RF| ~0.95                         | `budget`, `runtime`, `vote_average`, `revenue` | Baseline features should provide some signal              | Models show limited predictive power                        |
| 2         | Linear Regression, RF| LR: 1.02, RF: 0.96            | + `budget_per_minute`                         | Budget per minute might correlate better                  | Slight RF improvement, LR worse                            |
| 3         | Linear Regression, RF| LR: 1.00, RF: 0.95            | + `release_year`, `title_length`, `vote_ratio` | Time and vote strength should add signal                  | No major improvement                                        |
| 4         | Linear Regression, RF| both ~0.95                    | Only `vote_average`                           | Test if `vote_average` alone is strong enough             | Surprisingly powerful alone                                |
| 5         | Linear Regression, RF| both ~0.95                    | + top genres and studios                      | Content/producer info might be useful                     | Same RMSE, but more diverse features                       |
| 6         | Linear Regression, RF| RF: Train: 0.92, Test: 0.95   | Combined all features                         | Combination may stabilize variance                        | Stable, but `vote_average` dominates                       |
| 7         | RF + GridSearch      | Train: 0.93, Test: 0.95       | Same as It. 6 + tuned hyperparams             | Optimization should help                                 | Best performing model, but no breakthrough                |
| 8         | RF (no `vote_average`)| Train: 0.94, Test: 0.95       | Without `vote_average`                        | Fairer feature distribution for app deployment            | Same performance, better feature spread → used in app  |
---

## References  
**Top 5 Feature Importances (Final Model):**

- `release_year`
- `runtime`
- `budget`
- `top_genre_Drama`
- `top_studio_Warner Bros.`

