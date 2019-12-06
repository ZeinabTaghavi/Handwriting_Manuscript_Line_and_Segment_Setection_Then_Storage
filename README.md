## handwriting-Manuscript-_line_and_segment_detection_and_storage
### this project has 2 main parts: 1- line detection, 2- segment detection in manuscript

#### why should we do it?(Despite the presence of hOCR)
in Persian and Arabic texts hocr is not strong enough to detect lines and words(especially when vowels are written like مَخصوصاً)
this is hocr result **line detection**:

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/Comparison_codes/line_detection_hocr_or_x_y_projection/HW_hocr/1.jpg_rect_lines_with_hOCR.jpg?raw=true" width="50%" height="50%">

this is our code result **line detection**:

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/line_detectoin/1.jpg_find_line_by_semi_histogram_5_bound.jpg?raw=true" width="50%" height="50%">

this is hocr result **segment detection**:

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/Comparison_codes/segment_detectoin_hOCR_x_y_projection/rect_words_with_hOCR_EAST_on_denoised_img.jpg?raw=true" width="50%" height="50%">

this is our code result **segment detection**:

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/segment_detectoin/x_y_projection_contours/1.jpg_1_contoured.jpg?raw=true" width="50%" height="50%">

#### describing code:

source image:

<img src="https://raw.githubusercontent.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/master/line_detectoin/1.jpg" width="50%" height="50%">

##### 1- line detection:

by using x projection and then y projection we can find lines, in image what does it mean?
read below:
  ```
  # 2 - find the high compression vertical area

    vertical_hist = [sum(gray_env[i,:]) for i in range(img.shape[0])]
    
  ```
  this is result of vertical_hist:

  <img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/plots/plot1.png?raw=true" width="50%" height="50%">  
  
  ```
    vertical_temp = gray_corrected_rotation.copy()
    vertical_limit = gray_env.shape[1] * 255 * vertical_percent *.01
    for i in range(len(vertical_hist)):
        if vertical_hist[i] > vertical_limit:
            vertical_temp[i,:] = 255
        else:
            vertical_temp[i,:] = 0
            
  ```
  this is result of mapping high density parts to be main lines:
  
  <img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/plots/plot2.png?raw=true" width="50%" height="50%">
  
it would give us a multimodal histogram, gets us **height** of lines.

then in each line, with same way we can find correct location of lines.
  ```
  for y1,y2 in vertical_lines_positions:
        temp_img_env = gray_corrected_rotation_env[y1:y2,:]
        horizontal_limit = (y2-y1) * 255 * horizontal_percent * .01
        for j in range(temp_img_env.shape[1]):
            if sum(temp_img_env[:,j]) > horizontal_limit:
                line_location_image[y1:y2, j] = 0

  ```
  
then draw rectangle to bound them, and this is result:

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/line_detectoin/1.jpg_find_line_by_semi_histogram_5_bound.jpg?raw=true" width="50%" height="50%">

adn one of the stored lines:

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/segment_detectoin/x_y_projection_contours/1.jpg?raw=true" width="50%" height="50%">

and then, we will store them in folder.


##### 2- segment detection

at first, detect contours, in this time, may detect many noises,
so whot to removethem?
this is the histogram based on contours contourAre(lowest part is min contourAre and highest is biggest contourAre, in 10 bins):

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/plots/plot3.png?raw=true" height="50%" width="50%">

the first bin has highest count of contoursArea, they are noises or dots, and must be ignored,
then to cover all parts of segments(dots(like ب چ ج), vowels(like سَلام or بعضاً), and some seprate parts of one segments(like ک or گ )) detect first and last of width(w1, w1) then cover all heigh of line (h1 = 0 , h1 = height of line)
then result is this image

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/segment_detectoin/x_y_projection_contours/1.jpg_1_contoured.jpg?raw=true" height="50%" width="50%">

and store them in a seprate file, 
some of example segments are:

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/segment_detectoin/x_y_projection_contours/Segment_images_for_1.jpg/11_segment_y1_-14_y2_126_x1_639_x2_687_.jpg?raw=true" height="40%" width="40%">

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/segment_detectoin/x_y_projection_contours/Segment_images_for_1.jpg/14_segment_y1_-16_y2_125_x1_690_x2_729_.jpg?raw=true" height="40%" width="40%">

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/segment_detectoin/x_y_projection_contours/Segment_images_for_1.jpg/15_segment_y1_-13_y2_118_x1_311_x2_361_.jpg?raw=true" height="40%" width="40%">

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/segment_detectoin/x_y_projection_contours/Segment_images_for_1.jpg/17_segment_y1_-27_y2_143_x1_595_x2_634_.jpg?raw=true" height="40%" width="40%">

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/segment_detectoin/x_y_projection_contours/Segment_images_for_1.jpg/1_segment_y1_36_y2_117_x1_787_x2_817_.jpg?raw=true" height="40%" width="40%">

