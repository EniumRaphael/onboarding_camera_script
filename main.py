import cv2 as cv

def main():
	cap = cv.VideoCapture(2) # change here the number if the wrong camera is used

	cap.set(cv.CAP_PROP_SETTINGS, 1)

	width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

	print(f"{width=} / {height=}")

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
			print("Bisous bbye.")
			break
		elif key == 0x7f:	# backspace
			filename = filename[:-1]
		elif key == 0x0d:	# enter
			filename = filename.replace(' ', '-')

			print(f"Saving images/{filename}.jpg")

			cv.imwrite(f"images/{filename}.jpg", img)

			filename = ""
		elif key != -1:
			filename += chr(key)
	
	cap.release()


if __name__ == "__main__":
	main()