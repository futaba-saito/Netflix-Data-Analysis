#Importing pandas and matplotlib
import pandas as pd
import matplotlib.pyplot as plt

#Load the Netflix dataset from a CSV file into a pandas DataFrame
netflix = pd.read_csv("netflix_titles.csv")

#Explore the data
def explore_data(df):
    print("First 5 rows")
    print(df.head())

    print("\nDataset Information")
    df.info()

    print("\nSummary Statistics")
    print(df.describe())

    print("\nMissing Values")
    print(df.isnull().sum())

    print("Duplicate rows")
    print(df.duplicated().sum())

explore_data(netflix)

def clean_data(df):

    #Create a copy of the original dataset so the raw data remains unchanged throughout the cleaning and analysis process
    cleaned = df.copy()

    #Fill missing values to avoid errors during analysis and plotting
    cleaned["director"] = cleaned["director"].fillna("Unknown")
    cleaned["cast"] = cleaned["cast"].fillna("Unknown")
    cleaned["country"] = cleaned["country"].fillna("Unknown")
    cleaned["rating"] = cleaned["rating"].fillna("Not Rated")
    cleaned["duration"] = cleaned["duration"].fillna("Unknown")

    # Remove rows with missing dates because they cannot be used for
    # time-based analyses such as month or year content additions
    cleaned = cleaned.dropna(subset=["date_added"])

    #Remove unnecessary whitespace 
    cleaned["date_added"] = cleaned["date_added"].str.strip()

    #Convert date_added from text to datetime format
    cleaned["date_added"] = pd.to_datetime(cleaned["date_added"])

    return cleaned

cleaned_netflix = clean_data(netflix)

#Verify the cleaning
print("\nMissing values after cleaning")
print(cleaned_netflix.isnull().sum())

print("\nDataset Shape After Cleaning")
print(cleaned_netflix.shape)


#===================================================================
#Question 1: How many movies and shows are on Netflix?
#===================================================================

#Count movies vs TV shows
content_count = cleaned_netflix["type"].value_counts()

print("\nMovies vs TV Shows")
print(content_count)

movie_count = content_count["Movie"]
tv_count = content_count["TV Show"]
total_titles = movie_count + tv_count

movie_percentage = (movie_count/ total_titles) * 100

#Plot Movies vs TV Shows
plt.figure(figsize=(8,5))
content_count.plot(kind="bar")

plt.title("Number of Movies and TV Shows on Netflix")
plt.xlabel("Content Type")
plt.ylabel("Count")

plt.tight_layout()
plt.show()


print(f"\nApproximately {movie_percentage:.1f}% of Netflix's catalog consists of movies.")

#===================================================================
#Question 2: Which countries produce the most on Netflix content?
#===================================================================

#Exclude missing countries ("Unknown")
country_count = (cleaned_netflix[cleaned_netflix["country"] != "Unknown"]["country"] .value_counts().head(10))

#Count the top 10 countries
print("\nTop 10 countries")
print(country_count)

first_country = country_count.index[0]
second_country = country_count.index[1]

#Plot top 10 countries
plt.figure(figsize=(8,5))
country_count.plot(kind="bar")

plt.title("Top 10 Countries Producing the Most Netflix Content")
plt.xlabel("Country")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

print(f"\nInsight: {first_country} contributes the largest number of titles, followed by {second_country}.")

#==================================================================
#Question 3: How has Netflix grown over the years?
#==================================================================

# Count the number of titles released each year to identify
release_count = cleaned_netflix["release_year"].value_counts().sort_index()

print("\nNumber of Titles by Release Year")
print(release_count)

peak_year = release_count.idxmax()
peak_year_titles = release_count.max()

#plot the release year
plt.figure(figsize=(8,5))
release_count.plot(kind="line")

plt.title("Netflix Content by Release Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

plt.tight_layout()
plt.show()

print(
    f"\nInsight: Netflix's catalog contains the most titles released in {peak_year}, "
    f"with {peak_year_titles:,} titles."
    )

#========================================================================
#Question 4: Which month does Netflix add the most content?
#========================================================================

# Extract the month name from the date_added column for seasonal analysis
cleaned_netflix["month_added"] = cleaned_netflix["date_added"].dt.month_name()

#Store the months chronologically
month_order = [
    "January", "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December"
               ]

#Count content added by month
month_count = (cleaned_netflix["month_added"].value_counts().reindex(month_order))

print("\nMonth added")
print(month_count)

peak_month = month_count.idxmax()
peak_month_titles = month_count.max()

#Plot month added
plt.figure(figsize=(8,5))
month_count.plot(kind="bar")
plt.title("Titles Added by Month")
plt.xlabel("Month")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

print(
    f"\nInsight: Netflix adds the most content in {peak_month}, with {peak_month_titles}")

#=========================================================================
#Question 5: What are the most common genres?
#=========================================================================

# Split multiple genres into individual rows so that each genre can be counted separately
genres = cleaned_netflix["listed_in"].str.split(", ").explode()

genre_count = genres.value_counts().head(10)

print("\nTop 10 Genre")
print(genre_count)

top_genre = genre_count.index[0]
top_genre_count = genre_count.iloc[0]

genre_percentage = (top_genre_count/ len(cleaned_netflix))* 100

#Plot genres
plt.figure(figsize=(8,5))
genre_count.plot(kind="bar")

plt.title("Top 10 Genres on Netflix")
plt.xlabel("Genre")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


print(
    f"\nInsight: The most common genre on Netflix is {top_genre}, appearing in "
    f"{top_genre_count:,} titles ({genre_percentage:.1f}% of all Netflix titles)." 
    )