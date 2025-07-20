import cv2 as cv
import os
import logging

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s | [%(levelname)s] %(message)s',
	datefmt='%d-%m-%Y'
)

def list_cameras(max_tested=10):
	available = []
	for i in range(max_tested):
		cap = cv.VideoCapture(i)
		if cap is not None and cap.read()[0]:
			logging.debug(f"Caméra détectée. (id => {i})")
			available.append(i)
		cap.release()
	return available

def choose_camera():
	available = list_cameras()
	if not available:
		logging.critical("Aucune caméra détectée.")
		exit(1)

	print("Caméras disponibles :")
	for idx in available:
		print(f"[{idx}] /dev/video{idx}")

	while True:
		try:
			choice = int(input("Choisissez le numéro de la caméra : "))
			if choice in available:
				return choice
			else:
				print("Numéro invalide.")
		except ValueError:
			print("Veuillez entrer un nombre.")

def main():
	cam_index = choose_camera()
	cap = cv.VideoCapture(cam_index)


	cap.set(cv.CAP_PROP_SETTINGS, 1)

	width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

	logging.info(f"Caméra initialisée avec une résolution de {width}x{height}.")

	filename = ""
	while True:
		ret, img = cap.read()

		if not ret:
			raise RuntimeError("Cannot take a picture")
		
		ui = img.copy()

		cv.putText(ui, filename, (30, 50), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2)
		
		cv.imshow("Preview", ui)
		key = cv.waitKey(1)

		if key == 0x1b:		# escape
            logging.info("Bisous bbye.")
			break
		elif key == 0x7f:	# backspace
			filename = filename[:-1]
		elif key == 0x0d:	# enter
			filename = filename.replace(' ', '-')

			logging.info(f"Saving images/{filename}.jpg")

			os.makedirs("images", exist_ok=True)
			cv.imwrite(f"images/{filename}.jpg", img)

			filename = ""
		elif key != -1:
			filename += chr(key)
	
	cap.release()


if __name__ == "__main__":
	main()
