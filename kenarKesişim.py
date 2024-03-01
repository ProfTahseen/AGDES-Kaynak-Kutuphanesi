import cv2
import numpy as np

def kesisimleriBul(gorselPath):
    # Görseli siyah-beyaz olarak oku
    gorsel = cv2.imread(gorselPath, cv2.IMREAD_GRAYSCALE)

    # Canny kenar tespit algoritması
    kenarlar = cv2.Canny(gorsel, 50, 150, apertureSize=3)

    # Hough çizgi oylama/seçim algoritması
    cizgiler = cv2.HoughLines(kenarlar, 1, np.pi / 180, threshold=100)

    # Çizgileri siyah bir görselin üzerine çiz
    siyahGorsel = np.zeros_like(gorsel)
    if cizgiler is not None:
        for cizgi in cizgiler:
            rho, theta = cizgi[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(siyahGorsel, (x1, y1), (x2, y2), 255, 1)

    # Olasılıksal Hough kesişim tespiti
    kesisimler = cv2.HoughLinesP(siyahGorsel, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    # Görselin üzerine tespit edilen çizgileri çizme
    if kesisimler is not None:
        for line in kesisimler:
            x1, y1, x2, y2 = line[0]
            cv2.circle(gorsel, (x1, y1), 5, 255, -1)  # Kesişimleri noktalarla belirtme

    # Sonucu gösterme
    cv2.imshow(gorsel)
    cv2.waitKey()
    cv2.destroyAllWindows()

gorselPath = '' # Görsel dosya yolu
kesisimleriBul(gorselPath)
