import io
from google.cloud import vision

def detect_document(path):
    client = vision.ImageAnnotatorClient()

    # 이미지 파일을 열고 데이터를 바이너리 형태로 읽어들임.
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    # google vision api를 사용하여 해당 이미지에서 도큐먼트를 추출함.
    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    # 추출한 도큐먼트는 page > block > paragraph > word > symbol 순의 계층적인 구조를 가짐.
    document = ''
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    document += ''.join([symbol.text for symbol in word.symbols])
            document += '\n'

    # 추출한 도큐먼트를 'temp.txt'에 저장함.
    with io.open('temp.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(document)

if __name__ == '__main__':
    detect_document('test.jpg')
