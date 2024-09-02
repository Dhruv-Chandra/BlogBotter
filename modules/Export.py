import st_static_export as sse

def export(title, content):
    with open("css/result.css") as r:
        css_text = r.read()

    static_html = sse.StreamlitStaticExport(css=css_text)
    static_html.add_header(id="title",text=title, size="H1", header_class="head_cl")

    static_html.add_text(id="explanation", text=content, text_class='footn')

    str_result = static_html.create_html()
    return str_result