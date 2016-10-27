from bs4 import BeautifulSoup
import bs4

def parse_doc(filepath, output_path):
    with open(filepath, 'rb') as f, open(output_path, 'w', encoding='utf-8') as w:
        w.write("{% macro parsed_site() %}\n")
        data = BeautifulSoup(f.read(), 'html.parser')
        body = data.body
        print(str(body))
        for child in body.find_all():
            if type(child) == bs4.element.Tag and len(list(child.descendants)) == 1:
                if child.string is not None:
                    new_tag = data.new_tag("div", **{'class':'parser_select'})
                    child.wrap(new_tag)
        w.write(str(body))
        w.write("{% endmacro %}")

# def get_parsed_data(objects, filepath):
#     with open(filepath, 'rb') as f:


if __name__ == '__main__':
    print(parse_doc('test_input.html', 'test.html'))



