from lxml import etree
from bs4 import BeautifulSoup
import bs4
# parser = etree.HTML()

def split_tag(element):
    text = element.text
    pure_tag = etree.tostring(element).split()

def parse_doc(filepath, output_path):
    with open(filepath, 'rb') as f, open(output_path, 'w', encoding='utf-8') as w:
        w.write("{% macro parsed_site() %}\n")
        # w.write('<html>')
        data = BeautifulSoup(f.read(), 'html.parser')
        new_tag = BeautifulSoup('<html></html>', 'html.parser')
        body = data.body
        # w.write(str(data.head))
        for child in body.find_all():
            # for child in element.descendants:
            if type(child) == bs4.element.Tag and len(list(child.descendants)) == 1:
                # print(child)
                if child.string is not None:
                    new_tag = data.new_tag("div", **{'class':'parser_select'})
                    child.wrap(new_tag)
                        # break
        # new_tag.append(data.head)
        # new_tag.append(data.body)
        w.write(str(body))
        # w.write('</html>')
        w.write("{% endmacro %}")
    # return str(body).strip('<body>').strip('</body>')

if __name__ == '__main__':
    print(parse_doc('test_input.html', 'test.html'))



