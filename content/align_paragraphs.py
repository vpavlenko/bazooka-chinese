import bs4

soup = bs4.BeautifulSoup(open('hpmor_en.html').read(), "html.parser")

english_paragraphs = soup.find_all('p')
