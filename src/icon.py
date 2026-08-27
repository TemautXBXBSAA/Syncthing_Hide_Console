from PIL import Image
import zlib
import base64
from typing import Union
def encode_icon(icon_path: Union[str, Image.Image], split_len: int = 50) -> str:
    if isinstance(icon_path, str):
        with Image.open(icon_path) as original_img:
            if original_img.mode != 'RGBA':
                img = original_img.convert('RGBA')
            else:
                img = original_img.copy()
    elif isinstance(icon_path, Image.Image):
        if icon_path.mode != 'RGBA':
            img = icon_path.convert('RGBA')
        else:
            img = icon_path
    else:
        raise ValueError("Invalid icon path or image")
    
    try:
        width, height = img.size
        raw_data = img.tobytes()
        compressed_data = zlib.compress(raw_data, level=9)
        b85_encoded = base64.b85encode(compressed_data).decode('ascii')
        formatted_str = '\n'.join([
            b85_encoded[i:i+split_len] 
            for i in range(0, len(b85_encoded), split_len)
        ])
        
        header = f"{width},{height} "
        return header + formatted_str
        
    finally:
        if isinstance(icon_path, Image.Image):
            img.close()

def decode_icon(encoded_string: str) -> Image.Image:
    try:
        lines = encoded_string.split(' ', 1)
        if len(lines) < 2:
            raise ValueError("Invalid encoded string format")
        
        header = lines[0]
        b85_data = lines[1].replace("\n", "")
        try:
            width, height = map(int, header.split(','))
        except ValueError:
            raise ValueError("Invalid header format")
        compressed_data = base64.b85decode(b85_data)
        raw_data = zlib.decompress(compressed_data)
        expected_length = width * height * 4
        if len(raw_data) != expected_length:
            raise ValueError(
                f"Data length mismatch: expected {expected_length}, got {len(raw_data)}"
            )
        img = Image.frombytes('RGBA', (width, height), raw_data)
        return img
    except Exception as e:
        raise ValueError(f"Failed to decode icon: {str(e)}") from e
    
if __name__ == "__main__":
    icon = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
    print(encode_icon(icon))