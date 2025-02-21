import fileinput
import re

def process_headers(line):
    pattern = r"^\s*(#{1,6})\s+(.*)$"
    match = re.match(pattern, line)
    if match:
        level = len(match.group(1))
        return f"<h{level}>{match.group(2).strip()}</h{level}>\n"
    return line

def process_bold_text(line):
    pattern = r"(\*\*|__)([^\*]+?)\1"
    return re.sub(pattern, r"<b>\2</b>", line)

def process_italic_text(line):
    pattern = r"(\*|_)([^\*]+?)\1"
    return re.sub(pattern, r"<i>\2</i>", line)

def process_images(line):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.sub(pattern, r'<img src="\2" alt="\1"/>', line)

def process_links(line):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.sub(pattern, r'<a href="\2">\1</a>', line)

def handle_ordered_lists(lines: list[str]):
    result = []
    inside_list = False
    
    for line in lines:
        if line.startswith("<li>"):
            if not inside_list:
                result.append("<ol>\n")
                inside_list = True
            result.append(line)
        else:
            if inside_list:
                result.append("</ol>\n")
                inside_list = False
            result.append(line)
    
    if inside_list:
        result.append("</ol>\n")
    
    return result

def process_numbered_lists(line):
    pattern = r"^\s*\d+\.\s+(.*)$"
    match = re.match(pattern, line)
    if match:
        return f"<li>{match.group(1).strip()}</li>\n"
    return line

def convert_markdown(markdown):
    markdown = [process_headers(line) for line in markdown]
    markdown = [process_bold_text(line) for line in markdown]
    markdown = [process_italic_text(line) for line in markdown]
    markdown = [process_images(line) for line in markdown]
    markdown = [process_links(line) for line in markdown]
    markdown = [process_numbered_lists(line) for line in markdown]
    markdown = handle_ordered_lists(markdown)
    return markdown

def main():
    print("".join(convert_markdown(fileinput.input())))
    # creating a file called result.html
    with open("result.html", "w") as file:
        file.write("".join(convert_markdown(fileinput.input())))

if __name__ == "__main__":
    main()
