# X Tweet Scheduler

X Tweet Scheduler is a Python-based tool that automates the process of posting tweets on X (formerly Twitter) using the Tweepy library. This repository includes scripts for posting tweets and a GitHub Actions workflow for scheduling tweets to be posted automatically at specified times.

## Explanation of the Sections:

- **Overview**: Describes the purpose of the repository and the main components.
- **Setup**: Provides detailed steps for cloning the repository, installing dependencies, configuring credentials, creating necessary files, and setting up GitHub Actions.
- **Workflow**: Explains how the tweet posting and scheduling works.
- **Testing**: Provides instructions for running unit tests to ensure everything functions as expected.
- **Customization**: Instructions for adjusting the schedule and updating the tweet content.
- **Contributing**: Invites contributions and provides contact information.
- **License**: Indicates the project’s licensing terms.

## Overview

- **`tweets.py`**: Contains a list of predefined tweets to be posted.
- **`config.py`**: Configuration file for Twitter API credentials.
- **`main.py`**: The main script that handles tweeting and logging.
- **GitHub Actions**: Automates the tweet posting process according to a specified schedule.

## Setup

1. **Clone the Repository:**

   Clone this repository to your local machine using Git:

   ```bash
   git clone https://github.com/MohdMuslim92/x-tweet-scheduler.git
   cd x-tweet-scheduler
   ```
   
2. **Install Dependencies:**

Install the necessary Python packages using pip:

```
pip install -r requirements.txt
```

3. **Configure Twitter API Credentials:**

Create a .env file in the root directory of the repository with the following content:

```
API_KEY=your_api_key
API_SECRET_KEY=your_api_secret_key
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
BEARER_TOKEN=your_bearer_token
```
Replace your_api_key, your_api_secret_key, your_access_token, your_access_token_secret, and your_bearer_token with your actual Twitter API credentials.

4. **Create tweet_log.txt:**

The `tweet_log.txt` file is used for logging tweet activity and errors. This file will be created automatically when the main.py script runs. Ensure that the script has write permissions to the directory where it is executed.

5. **Set Up GitHub Actions:**

This repository includes a GitHub Actions workflow to automate the tweet posting. The workflow is defined in .github/workflows/tweet-scheduler.yml. It is configured to run at specified times (adjust as needed).

To use GitHub Actions, ensure the workflow is set up in your repository:

* Go to your repository on GitHub.
* Navigate to the Actions tab.
* Ensure the workflow runs as expected based on your cron schedule.

6. **Run the Script Locally (Optional):**

You can manually run the `main.py` script to test it before relying on the GitHub Actions:

```
python main.py
```
This will post tweets from the list defined in tweets.py and log the results to tweet_log.txt.

## Workflow

* **Tweet Posting:** The main.py script authenticates with the Twitter API and posts tweets from the predefined list. It logs the outcome of each tweet to tweet_log.txt.
* **GitHub Actions:** Automatically schedules and posts tweets based on the defined schedule in .github/workflows/tweet-scheduler.yml.

## Testing
Unit tests are included to ensure the functionality of the main.py script:

1. **Run Unit Tests:**

To run the tests and ensure everything works correctly, use the following command:

```
python -m unittest test_main.py
```
This will execute all the tests in test_main.py and report any issues.

2. **Code Quality Checks:**

The project uses pylint to enforce coding standards and style guidelines. To check the code quality, run:

```
pylint config.py main.py test_main.py
```

## Customization

* **Adjust Tweet Schedule:** Modify the cron schedule in the GitHub Actions workflow file to fit your posting preferences.
* **Update Tweets:** Edit the tweets.py file to change or add tweets to be posted.

## Contributing

Feel free to submit issues or pull requests to improve this project. For any questions or feedback, please contact mohammed.muslim2022@gmail.com.

## License

This project is licensed under the MIT License.


Feel free to adjust the instructions according to your specific requirements or preferences.
