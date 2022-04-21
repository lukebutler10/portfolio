import os
import random
import re
import sys
import numpy as np

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
    output_list = dict()

    if len(corpus[page]) == 0: #here we consider case where the page inputted doesn't link to any others
    	for page_x in corpus:
    		output_list.update({page_x : 1/len(corpus)}) #we choose the link randomly from all pages, including the current page
    	return output_list

    for page_x in corpus:
        output_list.update({page_x:(1-damping_factor)/len(corpus)}) #this turns output_list from empty dictionary to one with pages as keys and (1-d)/n (currently) as values each page


    for page_x in corpus:
        if page_x in corpus[page]:
            output_list[page_x] += damping_factor/len(corpus[page])
            
    return(output_list)

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    count_dict = {page_x:0 for page_x in corpus} #will use this to count occurences of surfer visiting each page

    x = 1
    while x <= n:
        if x == 1:
            page = random.choice(list(corpus)) #choosing a page to start on at random
            count_dict[page] +=1
            x +=1
        else: 
            page = np.random.choice(list(corpus),1,p=[transition_model(corpus,page,damping_factor)[page_x] for page_x in corpus])[0]
            count_dict[page] += 1
            x +=1
            
    return {page_x:count_dict[page_x]/n for page_x in corpus}


    raise NotImplementedError



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus) #defining n as no. of pages
    iter_pr = {page:1/n for page in corpus}
    diff_dict = {page:1000 for page in corpus}
    largest_diff = 1000

    def links_list(page): #returns a list of pages that have a link to the user-given "page"
    	links = []
    	for page_x in corpus:
    		if page in corpus[page_x]:
    			links.append(page_x)
    	return links
    
    def iter_value(page):
        return (1-damping_factor)/n + damping_factor * (sum([iter_pr[page_x]/len(corpus[page_x]) for page_x in links_list(page)]))

    while largest_diff > 0.001:
        new_iter_pr = {page:iter_value(page) for page in corpus}
        for page in corpus:
            diff_dict[page] = abs(new_iter_pr[page]-iter_pr[page])
        iter_pr = new_iter_pr
        largest_diff = max(diff_dict.values())

    return iter_pr







    raise NotImplementedError




if __name__ == "__main__":
    main()
