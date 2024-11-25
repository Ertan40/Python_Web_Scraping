import requests


def get_hackernews_story(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        raise Exception(f"Not able to retrieve data due to an error: {str(error)}")


def hackernews_top_stories(max_stories: int = 10):
    """
    Get the top max_stories posts from HackerNews - https://news.ycombinator.com/
    :param max_stories:
    :return:
    """
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    try:
        story_ids = requests.get(url, timeout=10).json()[:max_stories]
    except requests.exceptions.RequestException as error:
        raise Exception(f"Error fetching top stories: {str(error)}")

    stories = []
    for story_id in story_ids:
        try:
            story = get_hackernews_story(story_id)
            stories.append(story)
        except Exception as e:
            print(f"Failed to fetch story {story_id}: {str(e)}")  # Log error and continue
    return stories


# Usage
def hackernews_top_stories_as_markdown(max_stories: int = 10):
    stories = hackernews_top_stories(max_stories)
    markdown = ""
    for story in stories:
        # Ensure title and url exist before formatting
        title = story.get('title', 'No Title')
        url = story.get('url', f"https://news.ycombinator.com/item?id={story['id']}")
        markdown += f"* [{title}]({url})\n"
    return markdown


if __name__ == "__main__":
    print(hackernews_top_stories_as_markdown())


# Output: * [Internet Archive: Security breach alert](
# https://www.theverge.com/2024/10/9/24266419/internet-archive-ddos-attack-pop-up-message) * [OS/2 TCPBEUI Name
# Resolution](https://www.os2museum.com/wp/os-2-tcpbeui-name-resolution/) * [Dookie Demastered](
# https://www.dookiedemastered.com/) * [Why Gov.uk's Exit this Page component doesn't use the Escape key](
# https://beeps.website/blog/2024-10-09-why-govuk-exit-this-page-doesnt-use-escape/) * [On 17th century "cocaine"](
# https://resobscura.substack.com/p/on-17th-century-cocaine) * [An n-ball Between n-balls](
# https://www.arnaldur.be/writing/about/an-n-ball-between-n-balls) * [Scrum's "Product Owner" Problem – By Adam Ard](
# https://rethinkingsoftware.substack.com/p/scrums-product-owner-problem) * [Nixiesearch: Running Lucene over S3,
# and why we're building a new search engine](https://nixiesearch.substack.com/p/nixiesearch-running-lucene-over-s3)
# * [The Strict Aliasing Situation Is Pretty Bad (2016)](https://blog.regehr.org/archives/1307)
# * [Zod:TypeScript-first schema validation with static type inference](https://zod.dev/)