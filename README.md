# Image-scrapper-for-deep-learning
Downloading images upon links and creating structured dataset ready for deep learning algorythms training.

## Img_net_parse.py:
Downloads images from web, using the list of direct links (which you can download free from ImageNet).

## Equaliser.py:
Makes the number of images for each category within all directories (training, validation, samples) equal to fit the CNN training algorythms.

‘categories’ directory contains test .txt files with small number of links so you could test it right away.
Just run the Img_net_parse.py within the location where it sits when unzipped.
One little thing - if you wish to try it on another images – names of .txt files shall be recorded in categories.csv line by line; there are no limits in classes of images, however the more of them – the longer it will take to upload.
