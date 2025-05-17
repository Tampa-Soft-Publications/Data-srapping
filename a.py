import requests
s = "https://catalog.usf.edu/preview_course_nopop.php?catoid=23&coid="
from bs4 import NavigableString, Tag
from bs4 import BeautifulSoup
import json



def parse_course_block(course_html, link):
    soup = BeautifulSoup(course_html, "html.parser")

    course = {
        "course_code": "",
        "course_title": "",
        "credits": 0,
        "description": "",
        "course_attributes": [],
        "un_sdgs": [],
        "prerequisites": [],
        "corequisites": [],
        "restrictions": [],
        "notes": ""
    }

    # Course Code and Title
    title_elem = soup.find("h1", id="course_preview_title")
    if title_elem:
        title_text = title_elem.get_text(strip=True)
        if " - " in title_text:
            code, title = title_text.split(" - ", 1)
            a = title.strip()
            a.replace("\xa0", ' ')
            course["course_title"] = a
            course["course_code"] = title[0:8]
        else:
            a = title_text.strip()
            a.replace("\xa0", ' ')
            course["course_title"] = a
            course["course_code"] = title_text[0:8]

    # Credits
    credit_strong = soup.find("strong", string=lambda s: s and "Credit(s):" in s)
    if credit_strong:
        next_strong = credit_strong.find_next("strong")
        if next_strong:
            try:
                course["credits"] = int(next_strong.get_text(strip=True))
            except ValueError:
                course["credits"] = 0

    # Description (safe version)
    """
    description = ""
    if credit_strong:
        node = credit_strong
        while node:
            node = node.next_sibling
            if node is None:
                break
            if getattr(node, 'name', None) == 'strong':
                break  # Stop at next bold section
            if isinstance(node, str):
                description += node.strip() + " "
            elif node.name == "br":
                continue
            else:
                text = node.get_text(strip=True)
                if text:
                    description += text + " "

    course["description"] = description.strip()
    """
    credit_strong = soup.find("strong", string=lambda s: s and "Credit(s):" in s)
    if credit_strong:
        # Find the next <strong> after the one with "Credit(s):"
        next_strong = credit_strong.find_next("strong")
        if next_strong:
            # Find the <br> that follows this next <strong>
            next_br = next_strong.find_next("br")
            if next_br and next_br.next_sibling:
                # Extract the content following the <br> tag
                n = str(next_br.next_sibling).find("<strong>")
                if n >= 0:
                    course["description"] = "None"
                else:
                    m = str(next_br.next_sibling).find("<a")
                    if m >= 0:
                        course["prerequisites"] = [a.get_text(strip=True) for a in next_br.next_sibling.find_all("a")]
                    else:
                        br_text = next_br.next_sibling.strip()
                        course["description"] = br_text

    # Course Attributes
    attr_strong = soup.find("strong", string=lambda s: s and "Course Attribute(s):" in s)
    if attr_strong:
        attr_text = attr_strong.next_sibling
        if attr_text:
            course["course_attributes"] = [a.strip() for a in attr_text.split(",")]
    #pre-req
    attr_strong = soup.find("strong", string=lambda s: s and "Prerequisite(s):" in s)
    if attr_strong:
        text_parts = []

        # Go through each sibling after the <strong> until you hit a <br>
        for sibling in attr_strong.next_siblings:
            if isinstance(sibling, Tag) and sibling.name == "br":
                break
            elif isinstance(sibling, NavigableString):
                text_parts.append(sibling.strip())
            elif isinstance(sibling, Tag):
                text_parts.append(sibling.get_text(strip=True))
        full_text = ' '.join(part for part in text_parts if part)
        if full_text:
            course["prerequisites"] = full_text
    #co-req
    attr_strong = soup.find("strong", string=lambda s: s and "CoPrerequisite(s):" in s)
    if attr_strong:
        text_parts = []

        # Go through each sibling after the <strong> until you hit a <br>
        for sibling in attr_strong.next_siblings:
            if isinstance(sibling, Tag) and sibling.name == "br":
                break
            elif isinstance(sibling, NavigableString):
                text_parts.append(sibling.strip())
            elif isinstance(sibling, Tag):
                text_parts.append(sibling.get_text(strip=True))
        full_text = ' '.join(part for part in text_parts if part)
        if full_text:
            course["corequisites"] = full_text
                                      
    # UN SDGs
    sdg_strong = soup.find("strong", string=lambda s: s and "UN SDG" in s)
    if sdg_strong:
            ul = sdg_strong.find_next("ul")
            if ul:
                course["un_sdgs"] = [li.get_text(strip=True) for li in ul.find_all("li")]
    course["link"] = str(link)

    #Notes
    attr_strong = soup.find("strong", string=lambda s: s and "Other Information" in s)
    if attr_strong:
        attr_text = attr_strong.next_sibling
        if attr_text:
            course["notes"] = attr_text
    #restrictions
    restrictions_strong = soup.find("strong", string=lambda s: s and "Restriction(s):" in s)

    if restrictions_strong:
        # Find the first <ul> tag immediately following the <strong>
        ul_tag = restrictions_strong.find_next_sibling("ul")
        if ul_tag:
            # Extract visible text from each <li> inside the <ul>
            restrictions = [li.get_text(strip=True) for li in ul_tag.find_all("li")]
            if restrictions:
                course["restrictions"] = restrictions
            
    return course


# --- Example usage ---
if True:


    with open('usf_class.json', 'w') as f:

        for i in range(101584, 104855):
            s1 = s+str(i)
            headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36"
            }
            html = requests.get(s1, headers=headers)
            soup = BeautifulSoup(html.text, 'html.parser')
    

            td_tag = soup.find('td', class_='block_content_outer')
            course_data = parse_course_block(str(td_tag), s1)
            print(course_data)
            f.write(str(course_data) + "\n")    
        


