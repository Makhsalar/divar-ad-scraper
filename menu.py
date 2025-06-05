"""
This script provides an interactive menu to generate URLs for scraping real estate ads
from Divar (Babolsar city) based on selected categories and subcategories.
"""


def display_menu_and_get_url():
    """
    Display the main menu options, get user choice,
    and return the corresponding URL for scraping ads from Divar.
    """
    base_url_prefix = "https://divar.ir/s/babolsar/"

    categories_config = {
        "0": ("all ads", "real-estate"),
        "1": ("buy-residential", "buy-residential"),
        "2": ("rent-residential", "rent-residential"),
        "3": ("buy-commercial-property", "buy-commercial-property"),
        "4": ("rent-commercial-property", "rent-commercial-property"),
        "5": ("rent-temporary", "rent-temporary"),
        "6": ("real-estate-services", "real-estate-services"),
    }

    subcategories_config = {
        "1": [
            ("the sub-category itself", "buy-residential"),
            ("apartment", "buy-apartment"),
            ("villa", "buy-villa"),
            ("old-house", "buy-old-house"),
        ],
        "2": [
            ("the sub-category itself", "rent-residential"),
            ("apartment", "rent-apartment"),
            ("villa", "rent-villa"),
        ],
        "3": [
            ("the sub-category itself", "buy-commercial-property"),
            ("office", "buy-office"),
            ("store", "buy-store"),
            (
                "industrial-agricultural-property",
                "buy-industrial-agricultural-property",
            ),
        ],
        "4": [
            ("the sub-category itself", "rent-commercial-property"),
            ("office", "rent-commercial-property"),
            ("store", "rent-store"),
            (
                "industrial-agricultural-property",
                "rent-industrial-agricultural-property",
            ),
        ],
        "5": [
            ("the sub-category itself", "rent-temporary"),
            ("temporary-suite-apartment", "rent-temporary-suite-apartment"),
            ("temporary-villa", "rent-temporary-villa"),
            ("temporary-workspace", "rent-temporary-workspace"),
        ],
        "6": [
            ("the sub-category itself", "real-estate-services"),
            ("contribution-construction", "contribution-construction"),
            ("pre-sell-home", "pre-sell-home"),
        ],
    }

    print("Welcome\nSelect a category for scraping ads from Divar (Babolsar)")
    for key, (display_name, _) in categories_config.items():
        print(f"{key} - {display_name}")

    while True:
        choice = input("Enter your choice (0-6): ")
        if choice in categories_config:
            break
        print("Invalid choice. Please try again.")

    selected_slug = ""
    if choice == "0":
        selected_slug = categories_config[choice][1]
    elif choice in subcategories_config:
        print(f"Subcategories for {categories_config[choice][0]}:")
        current_sub_options = subcategories_config[choice]
        for idx, (display_name, _) in enumerate(current_sub_options, 1):
            print(f"{idx} - {display_name}")

        while True:
            sub_choice_str = input(
                f"Enter subcategory number (1-{len(current_sub_options)}): "
            )
            try:
                sub_choice_idx = int(sub_choice_str)
                if 1 <= sub_choice_idx <= len(current_sub_options):
                    selected_slug = current_sub_options[sub_choice_idx - 1][1]
                    break
                print("Invalid subcategory number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        selected_slug = categories_config[choice][1]

    if selected_slug:
        return base_url_prefix + selected_slug

    print("Error: Could not determine the URL.")
    return None


if __name__ == "__main__":
    # Test the menu and URL generation
    target_url = display_menu_and_get_url()
    if target_url:
        print(f"\nSelected URL for scraping: {target_url}")
