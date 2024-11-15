from main_functions import extract_title, copy_static, generate_pages_recursive


def main():
    copy_static('./static', './public')
    generate_pages_recursive('./content', './template.html', './public')


if __name__ == "__main__":
    main()
