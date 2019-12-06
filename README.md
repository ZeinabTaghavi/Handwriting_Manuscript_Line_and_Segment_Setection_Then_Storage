## handwriting-Manuscript-_line_and_segment_detection_and_storage
### this project has 2 main parts: 1- line detection, 2- segment detection in manuscript

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

  <img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/plots/plot1.png?raw=true" width="100%" height="100%">  
  
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
  
  <img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/plots/plot2.png?raw=true" width="100%" height="100%">
  
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

<img src="https://github.com/ZeinabTaghavi/handwriting-Manuscript-_line_and_segment_detection_and_storage/blob/master/line_detectoin/lines_images_for_1.jpg/11_line_y1_1758_y2_1898_x1_2026_x2_2994_.jpg?raw=true" width="50%" height="50%">

and then, we will store them in folder.


##### 2- segment detection
