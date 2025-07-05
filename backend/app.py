from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import os
#from surya.recognition import RecognitionPredictor
#from surya.detection import DetectionPredictor
#from paddleocr import PaddleOCR
import easyocr
import torch

# # GPU/CPU choice
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")
# # Initialize Surya Model
# recognition_predictor = RecognitionPredictor()
# recognition_predictor.to(device)
# print("✅ Recognition model loaded")
# detection_predictor = DetectionPredictor()
# detection_predictor.to(device)
# print("✅ Detection model loaded")

reader = easyocr.Reader(['ja', 'en'], gpu=False)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

# Assign the tesseract ocr path
# pytesseract.pytesseract.tesseract_cmd = r"D:\OCR\path\tesseract.exe"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/ocr", methods=["POST"])
def ocr():
    if "images" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    files = request.files.getlist("images")
    results = {}

    for file in files:
        if not allowed_file(file.filename):
            results[file.filename] = "Invalid file format"
            continue
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        try:
            # # Basic Tesseract OCR
            # with Image.open(file_path) as image:
            #     # text = pytesseract.image_to_string(image, lang="chi_sim+jpn").strip()
            #     # results[file.filename] = text if text else "No text detected"

            #     ocr_data = pytesseract.image_to_data(image, lang="chi_sim+jpn", output_type=pytesseract.Output.DICT)
            #     n_boxes = len(ocr_data["text"])
            #     positioned_text = []
            #     for i in range(n_boxes):
            #         word = ocr_data["text"][i].strip()
            #         if word:
            #             positioned_text.append({
            #                 "text": word,
            #                 "x": ocr_data["left"][i],
            #                 "y": ocr_data["top"][i],
            #                 "width": ocr_data["width"][i],
            #                 "height": ocr_data["height"][i]
            #             })
            #         results[file.filename] = positioned_text
            
            # # Surya OCR
            # with Image.open(file_path) as image:
            #     preds = recognition_predictor([image], [None], detection_predictor)
            #     lines = sorted(preds[0].text_lines, key=lambda x: x.bbox[1])
            #     full_text = "\n".join(line.text for line in lines)
            #     # results[file.filename] = full_text

            #     positioned_text = []
            #     for line in lines:
            #         result = {
            #             "text": line.text,
            #             "x": line.bbox[0],
            #             "y": line.bbox[1],
            #             "width": line.bbox[2] - line.bbox[0],
            #             "height": line.bbox[3] - line.bbox[1]
            #         }
            #         positioned_text.append(result)
            #     results[file.filename] = positioned_text


            # EasyOCR
            with Image.open(file_path) as image:
                # result = reader.readtext(file_path)
                # full_text = "\n".join([text[1] for text in result])  # 提取文本
                # results[file.filename] = full_text if full_text else "No text detected"

                results_easyocr = reader.readtext(file_path)
                positioned_text = []
                for bbox, text, conf in results_easyocr:
                    x_min = min([point[0] for point in bbox])
                    y_min = min([point[1] for point in bbox])
                    width = max([point[0] for point in bbox]) - x_min
                    height = max([point[1] for point in bbox]) - y_min
                    
                    if text.strip():  # 过滤空文本
                        positioned_text.append({
                            "text": text,
                            "x": int(x_min),
                            "y": int(y_min),
                            "width": int(width),
                            "height": int(height),
                            "confidence": round(conf, 2)
                        })
                results[file.filename] = positioned_text

            # PaddleOCR
            # result = ocr.ocr(file_path, cls=True)
            # all_text = []
            # for line in result[0]:  # 第0个是图片结果
            #     text = line[1][0]  # line[1] 是识别结果，[0] 是文字内容
            #     all_text.append(text)
            # results[file.filename] = "\n".join(all_text) if all_text else "No text detected"

        except Exception as e:
            results[file.filename] = f"Error: {str(e)}"
        finally:
            os.remove(file_path)
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
