from image_capture import capture_image
from vision_api import analyze_image
from property_extractor import extract_properties
from data_formatter import format_item_data
from database import store_item

def main():
    # image = capture_image()
    image = '/home/ravi/code/projects/vision/data/images/IMG_5179.jpeg'
    
    vision_data = analyze_image(image)
    
    properties = extract_properties(vision_data)
    
    item_data = format_item_data(properties)
    
    store_item(item_data)


if __name__ == "__main__":
    main()