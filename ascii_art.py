import json
from PIL import Image

def create_ascii(img_path):
  pic = Image.open(img_path)
  width, height = pic.size
  aspect_ratio = height / width
  new_width = 110
  new_height = int(aspect_ratio * new_width)
  img = pic.resize((new_width, new_height))
  img = img.convert('L')
  pixels = img.getdata()
  chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']
  count = len(chars)
  new_pixels = [chars[int(((count - 1) * pixel) / 256)] for pixel in pixels]
  new_pixels = ''.join(new_pixels)
  new_pixels_count = len(new_pixels)
  ascii_image = [new_pixels[index : index + new_width] for index in range(0, new_pixels_count, new_width)]
  ascii_image = '\n'.join(ascii_image)
  return ascii_image + '\n'


def create_new_dict(old_dict):
  new_dict = {}
  for key in old_dict:
    nested_dict = old_dict[key]
    new_key = parse_title(nested_dict)
    new_dict[new_key] = nested_dict
  for key in new_dict:
    nested_dict = new_dict[key]
    img_path = nested_dict['path']
    nested_dict['ascii'] = create_ascii(img_path)
  return new_dict

def parse_title(d):
  txt = d['path']
  title = txt[12: -4]
  return title

def print_choices(d):
  print('\nEnter a number to see an ASCII image or "q" to quit:')
  for index, key in enumerate(d):
    print(f'{index + 1}) {key.title()}')

path = 'code/images.json'
with open(path, 'r') as f:
  data = json.load(f)

images = create_new_dict(data)
values = list(images.values())
correct_input = ['1', '2', '3', '4', '5', '6']

while True:
  print_choices(images)
  choice = input('> ')
  if choice == 'q':
    print('Thanks for looking')
    break
  elif choice in correct_input:
    index = int(choice) - 1
    print(values[index]['ascii'])
