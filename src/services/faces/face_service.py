import cv2
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model
import numpy as np
from typing import Union
import os


class FaceSwapper:
    def __init__(self, main_face_img: Union[str, np.ndarray]):
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        model_path = os.path.expanduser('~/.insightface/models/inswapper_128.onnx')
        self.swapper = get_model(model_path)
        # Если передается путь к изображению в виде строки, считываем изображение
        if isinstance(main_face_img, str):
            self.main_face_img = cv2.imread(main_face_img)
        else:
            self.main_face_img = main_face_img
        # Предполагаем, что в main_face_img только одно лицо
        main_faces = self.app.get(self.main_face_img)
        print("asdadasd")
        if len(main_faces) != 1:
            raise ValueError("The provided main face image should contain exactly one face.")
        self.main_face_info = main_faces[0]

    def swap_face(self, img: Union[str, np.ndarray]) -> np.ndarray:
        # Если передается путь к изображению в виде строки, считываем изображение
        if isinstance(img, str):
            img = cv2.imread(img)

        # Получаем все лица на изображении
        faces = self.app.get(img)
        if not faces:
            raise ValueError("No faces detected in the image for swapping.")

        # Заменяем все лица на "главное" лицо
        imgnew = img.copy()
        for face in faces:
            imgnew = self.swapper.get(imgnew, self.main_face_info, face, paste_back=True)

        return imgnew

    def change_main_face(self, new_main_face_img: Union[str, np.ndarray]):
        # Если передается путь к изображению в виде строки, считываем изображение
        if isinstance(new_main_face_img, str):
            new_main_face_img = cv2.imread(new_main_face_img)

        # Предполагаем, что в new_main_face_img только одно лицо
        new_main_faces = self.app.get(new_main_face_img)
        if len(new_main_faces) != 1:
            raise ValueError("The provided new main face image should contain exactly one face.")
        self.main_face_img = new_main_face_img
        self.main_face_info = new_main_faces[0]


# Пример использования:
# создание экземпляра класса с изображением "главного" лица
current_dir = os.path.dirname(os.path.realpath(__file__))
main_face_path = os.path.join(current_dir, 'main_face.jpg')
swapper = FaceSwapper(main_face_path)

# подмена лиц на другом изображении
try:
    swapped_image = swapper.swap_face('target_face.jpg')
    cv2.imshow('Swapped Image', swapped_image[:, :, ::-1])  # cv2 работает с BGR, matplotlib с RBG
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except ValueError as e:
    print("Error:", e)

