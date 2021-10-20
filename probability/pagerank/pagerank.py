import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linked_pages = corpus[page]
    distribution = {}

    if linked_pages == set():
        distribution_value = 1 / len(corpus)
        for p in corpus.keys():
            distribution[p] = distribution_value
    else:
        linked_page_count = len(linked_pages)
        total_page_count = len(linked_pages) + 1
        distribution[page] = (1 - damping_factor) / total_page_count
        for linked_page in linked_pages:
            distribution[linked_page] = damping_factor / linked_page_count + (1 - damping_factor) / total_page_count

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    starting_page = random.choice(list(corpus.keys()))
    samples = {}
    for page in corpus:
        samples[page] = 0

    current_page = starting_page
    for i in range(n):
        model = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(model.keys()), list(model.values()))[0]
        samples[current_page] += 1

    ranks = {}
    for page in samples:
        ranks[page] = samples[page] / n

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    ranks = {}
    for page in corpus:
        ranks[page] = 1 / n

    repeat = True
    while repeat:
        old_ranks = ranks.copy()
        for page in corpus:
            ranks[page] = (1 - DAMPING) / n
            for link in corpus:
                if page in corpus[link]:
                    num_links = len(corpus[link])
                    ranks[page] += DAMPING * ranks[link] / num_links
                if not corpus[link]:
                    ranks[page] += DAMPING * ranks[link] / n

        repeat = False
        for rank in ranks:
            if abs(ranks[rank] - old_ranks[rank]) > 0.001:
                repeat = True
                break

    return ranks


if __name__ == "__main__":
    main()
