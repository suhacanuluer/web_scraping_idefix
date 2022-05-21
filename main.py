from bs4 import BeautifulSoup
import requests
import pandas as pd

page_number = 0;
finish_page = 1;
comment_number = 0
data = list()

while page_number < finish_page:
    books_url = "https://www.idefix.com/kategori/Kitap/Edebiyat/grupno=00055?ShowNotForSale=True&Page="+ str(page_number) + ""
    books_request = requests.get(books_url)
    books_html = BeautifulSoup(books_request.content,"lxml")

    books_div1 = books_html.find("div",attrs={"class":"no-margin productListNewBox boxes books clearfix"})
    books_div2 = books_div1.find("div",attrs={"class":"row"})
    books_list = books_div2.find_all("div",attrs={"class":"cart-product-box-view"})

    for book_html in books_list:
        book_link = "https://www.idefix.com/"+book_html.a.get("href")
        books_request = requests.get(book_link)

        book_page_html = BeautifulSoup(books_request.content,"lxml")
        comments_html = book_page_html.find_all("div",attrs={"class":"comment"})

        book_div1 = book_page_html.find("div",attrs={"class":"product-info hidden-lg hidden-md hidden-sm col-xs-12"})
        book_name = book_div1.find("h3",attrs={"style":"margin-bottom: 10px !important; margin-top: 0px;"}).get_text().replace('\n',"").replace(' ',"")

        if (len(comments_html) != 0):
            for comment_html in comments_html:
                comment = comment_html.find(id="reviewBody").get_text()
                data.append(dict(
                    book = book_name,
                    comment = comment
                    ))
                comment_number += 1
    page_number += 1
print("Comment number: "+ str(comment_number))
print(data)