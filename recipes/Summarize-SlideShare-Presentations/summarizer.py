import re
import Algorithmia

# get your API key at algorithmia.com/user#credentials
client = Algorithmia.client("your_api_key")

def extract_text(url):
    """Retrieve text content from URL."""
    algo = client.algo("util/ExtractText/0.1.1")
    response = algo.pipe(url).result
    return response


def get_slide_text(input):
    """Clean text content and return content only from slides."""
    text = extract_text(input)
    # Remove non-alphanumeric characters
    new_data = re.sub(
        r'[^0-9a-zA-Z . ]', ' ', text)

    # Find all the separate slides (slides are extracted with 1., 2.
    # preceding each slide)
    nums = re.findall(r'[1-9]\.|[1-9][0-9]\.', new_data)

    last_slide = nums[-1]

    # Look for text between 1. and the last slide
    cleaned_data = re.findall(r'1\..*(?=' + last_slide + r')', new_data)

    # Artificially create sentences that the summarizer needs.
    remove_slide_numbers = re.sub(
        r'[1-9]\.|[1-9][0-9]\.', '.', str(cleaned_data))

    # Remove extra whitespace
    super_clean = ' '.join(str(remove_slide_numbers.lower()).split())
    return super_clean


def summarizer(input):
    """Summarize text content from slides."""
    data = get_slide_text(input)
    algo = client.algo('nlp/Summarizer/0.1.3')
    result = algo.pipe(data).result
    print("Summarizer output: ", result)

    # Add this code for step 5:
    try:
        # Write the text summary result to Dropbox
        client.file("dropbox://SlideSummary/slide_summary.txt").put(result)
        print("Printed contents to dropbox file")
    except Exception as e:
        print(e)


# Example Inputs
summarizer("http://www.slideshare.net/doppenhe/algorithmia-at-hackernews-meetup-seattle")
# summarizer("http://www.slideshare.net/MattKiser/algorithms-as-microservices")
