import cv2
import numpy as np

def yol_tespit_et(resim_yolu):

    img = cv2.imread(resim_yolu)
    siyah_resim = np.zeros_like(img)

    gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bulaniklastirilmis = cv2.GaussianBlur(img, (5, 5), 0)

    kenarlar = cv2.Canny(bulaniklastirilmis, 120, 200)

    genisletilmis_kenarlar = cv2.dilate(kenarlar, None, iterations=2)
    cv2.imshow(genisletilmis_kenarlar)

    hatlar = cv2.HoughLines(genisletilmis_kenarlar, 1, np.pi/180, threshold=500)
    cv2.imshow(kenarlar)

    if hatlar is not None:
        for hat in hatlar:
            rho, theta = hat[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 5)
            cv2.line(siyah_resim, (x1, y1), (x2, y2), (255, 255, 255), 5)

    cv2.imshow(img)
    cv2.imshow(siyah_resim)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

resim_yolu = ""
yol_tespit_et(resim_yolu)
