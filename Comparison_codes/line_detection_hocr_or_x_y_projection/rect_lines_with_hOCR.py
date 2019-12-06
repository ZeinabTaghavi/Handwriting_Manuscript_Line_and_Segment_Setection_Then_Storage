from lxml import etree
import cv2
import pytesseract

def find_line_by_hocr(file_name):

    img = cv2.imread(file_name,0)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    try:
        f = pytesseract.pytesseract.image_to_pdf_or_hocr(otsu , lang='ara+fas', extension='hocr')
    except:

        print('hOCR file was not found')

    tree = etree.fromstring(f)
    lines = tree.xpath("//*[@class='ocrx_word']")


    for line in lines:
        titles = line.attrib['title'].split()
        x1, y1, x2, y2 = int(titles[1]), int(titles[2]), int(titles[3]), int(titles[4].split(';')[0])
        otsu = cv2.rectangle(otsu , (x1 , y1) , (x2,y2) , (100,100,100) , 3)


    cv2.imwrite(file_name+'_rect_lines_with_hOCR.jpg',otsu)


if __name__ == '__main__':
    n1 = 1
    n2 = 6
    for i in range(n1,n2):
        img_file = str(i)+'.jpg'
        find_line_by_hocr(img_file)