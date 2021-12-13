# OpenCV VideoCropper<br/>
This module helps in processing videos using opencv.<br/>
How to use:<br/>
    from VideoCropper import VideoCropper<br/>
    Cropper = VideoCropper(<i>path</i>, ROI='1/2') # options are 1/2, 1/4, 1/8, LT, RT, LB, RB for different regions. if left none, will give a GUI to ask for region to crop.<br>
    Cropper.write()<br>
    Cropper.release()<br>
