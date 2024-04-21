import cv2

def face_replacer(image_name1, image_name2):
    # Загрузка изображений
    image1 = cv2.imread(image_name1)
    image2 = cv2.imread(image_name2)
    # Инициализация детектора лиц (например, с использованием Haar cascade)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Обнаружение лиц на изображениях
    faces1 = face_cascade.detectMultiScale(image1, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    faces2 = face_cascade.detectMultiScale(image2, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # Проверка наличия лиц
    if len(faces1) == 0 or len(faces2) == 0:
        print("Лица не обнаружены на одном из изображений.")
        exit()
    # Предполагается, что обнаружено только одно лицо на каждом изображении
    x1, y1, w1, h1 = faces1[0]
    x2, y2, w2, h2 = faces2[0]
    # Вырезаем области с лицами
    face1 = image1[y1:y1+h1, x1:x1+w1]
    face2 = image2[y2:y2+h2, x2:x2+w2]
    # Выравнивание лиц
    face1_resized = cv2.resize(face1, (h2, w2))
    face2_resized = cv2.resize(face2, (h1, w1))
    # Замена лиц
    image1[y1:y1+h1, x1:x1+w1] = face2_resized
    image2[y2:y2+h2, x2:x2+w2] = face1_resized
    # Вывод результатов
    # cv2.imshow('Image 1 with swapped face', image1)
    # cv2.imshow('Image 2 with swapped face', image2)
    cv2.imwrite(f'replaced_{image_name2}.jpg', image2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

face_replacer('image1.jpg', 'image2.jpg')