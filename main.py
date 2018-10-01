import io
import json
from google.cloud import vision
from google.protobuf.json_format import MessageToJson

def detect_document(path):
    client = vision.ImageAnnotatorClient()

    # 이미지 파일을 열고 데이터를 바이너리 형태로 읽어들임.
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    # google vision api를 사용하여 해당 이미지에서 도큐먼트를 추출함.
    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # 추출한 도큐먼트는 document > pages > blocks > paragraphs > words > symbols 순의 계층적인 구조를 가짐.
    text_data = ''
    for page in document.pages:
        vertex_x = 0
        for block in page.blocks:
            for paragraph in block.paragraphs:
                para_text = ''
                for word in paragraph.words:
                    for symbol in word.symbols:
                        text_data += symbol.text + ' : ' + str(symbol.bounding_box.vertices[0].x) + ', ' + str(symbol.bounding_box.vertices[0].y) + ' '
                        para_text += symbol.text
                        # if vertex_x - symbol.bounding_box.vertices[0].x > 10:
                        #     text_data += '\n'
                        # vertex_x = symbol.bounding_box.vertices[0].x
                        # text_data += symbol.text
                text_data += '\n\npara : ' + para_text + '\n\n'

    # 추출한 도큐먼트를 'temp.txt'에 저장함.
    with io.open('temp.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(text_data)

if __name__ == '__main__':
    detect_document('test.jpg')
