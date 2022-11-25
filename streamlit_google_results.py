import streamlit as st
import pandas as pd
import time
from requests_html import HTMLSession
from bs4 import BeautifulSoup




model_running = st.container()

input_data = st.form( 'form',)

with input_data:    
    url_input = st.text_input('page link',) 
    num_reuired_pages = st.number_input('number of pages' ,value=0, step= 1) 
    submitted = st.form_submit_button()

    


with model_running:
    

    

    st.title('ًloading google results')

    if submitted:

        
        s= HTMLSession()

        def getdata(url):
            r =s.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup

        def getnextpage (soup):
        
            

            page= soup.find_all('td' , {'class' : 'd6cvqb BBwThe'})
            
            nextpage= page[1].find('a')['href']
            
            if page[1].find('a')['id'] == 'pnnext':
                
                url = 'https://www.google.com' + str(nextpage)
                

                return url
            else:
                return
        

        soup = getdata(url_input)
        
        







        def collector(soup, url):
            google_pages = [url_input]
            
            i = 0 
            while i in range (num_reuired_pages):
                

                soup = getdata(url)
                url = getnextpage(soup)
                google_pages.append(url)
                i = i + 1
                        
            

                if not url:
                    break
            return google_pages

        google_results = collector (soup, url_input)  

        def google_soups (google_results):
            i = 0
            soups = []
            for i in range (len(google_results)):
                i = i+1
                r =s.get(google_results[i-1])
                soup = BeautifulSoup(r.text, 'html.parser')
                soups.append(soup)
                

            return soups

        google_soups = google_soups (google_results)

        def google_links_bypage (google_soups):
            links_by_page = []

            for i in range(len(google_soups)):
                i = i +1
                links = google_soups[i-1].find_all('div', {'class': 'yuRUbf'})
                
                links_by_page.append(links)
            return links_by_page  

        google_links_bypage = google_links_bypage(google_soups)


        def google_links_href (google_links_bypage):
            href_links_list = []

            i=0
        
            for i in range(len(google_links_bypage)):
                for n in google_links_bypage[i]:
                    

                    
                    
                        
                            
                    hrefs = n.find('a')['href']
                    href_links_list.append(hrefs)
                    i = i +1
                
            return href_links_list

        final_list = pd.DataFrame(google_links_href (google_links_bypage))  
        csv = final_list.to_csv()
        st.download_button( label="حمل النتائج",  data=csv,  file_name='نتائج جوجل .csv', mime='text/csv',)




