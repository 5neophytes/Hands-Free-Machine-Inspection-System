import cv2
import base64
import requests

# OpenAI API Key
api_key = "sk-proj-MugzvB91E6HoJee02kdwT3BlbkFJTQFtSA9C99xnXXVq5sXI"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to capture a photo
def capture_photo():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    print("Press 'c' to capture a photo or 'q' to quit.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture image.")
            break

        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1) & 0xFF
        photo_filename = 'captured_photo.png'
        cv2.imwrite(photo_filename, frame)
        print(f"Photo captured and saved as {photo_filename}")
        break
    
        # if key == ord('c'):
        #     photo_filename = 'captured_photo.png'
        #     cv2.imwrite(photo_filename, frame)
        #     print(f"Photo captured and saved as {photo_filename}")
        #     break
        # elif key == ord('q'):
        #     print("Quitting without capturing a photo.")
        #     break

    cap.release()
    cv2.destroyAllWindows()

    return photo_filename

# Function to detect number using OpenAI
def detect_number(image_path):
    # Encode the image to base64
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "How many fingers am I holding up? Only give the number as output."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        output = response.json()
        output_content = output['choices'][0]['message']['content']
        return output_content
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Main function to run the process
def main():
    photo_filename = capture_photo()
    
    if photo_filename:
        number = detect_number(photo_filename)
        
        if number is not None:
            print(f"Detected number: {number}")
        else:
            print("No number detected or error occurred.")

if __name__ == "__main__":
    main()
