
# coding: utf-8

# In[14]:

# use python 3 
# install new version of tensorflow (>1) 
# install opencv
# clone facenet from here: https://github.com/davidsandberg/facenet (suppose in your home folder)
# add ~/facenet/src to your PYTHONPATH
# mkdir ~/facenet/model/20170216-091149 and download weights from
#     https://drive.google.com/open?id=0B5MzpY9kBtDVSkRSZjFBSDQtMzA
# set base_addr path to the proper directory contains background and foreground iamge and member1.npy
# put this code (2A.py) into ~/facenet/src

import datetime
import sys
import time
import cv2
import align.detect_face as detect_face
from functools import wraps
import facenet
import tensorflow as tf
import numpy as np
from scipy import misc
import os

sys.path.append('/usr/local/lib')
min_area = 10000
base_addr = '/facenet/'
trained_model_dir = '../model/20170216-091149'
threshold = 1.22




#def fn_timer(function):
#    @wraps(function)
#    def function_timer(*args, **kwargs):
#        t0 = time.time()
#        result = function(*args, **kwargs)
#        t1 = time.time()
#        print ("Total time running %s: %s seconds" %
#               (function.func_name, str(t1-t0))
#               )
#        return result
#    return function_timer



print('Creating networks and loading parameters of face detection model...')
st = time.time()
with tf.Graph().as_default():
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.25)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    with sess.as_default():
        pnet, rnet, onet = detect_face.create_mtcnn(sess, None)
        print('time of loading face detection model is %f' % (time.time() - st))
        
        
st = time.time()
graph = tf.Graph()
with graph.as_default():
        sess = tf.Session()
        with sess.as_default():
            # load the model
            print("Loading Face Verification model...")
            meta_file, ckpt_file = facenet.get_model_filenames(os.path.expanduser(trained_model_dir))
            print("metafile and ckpt_files are %s and %s" % (meta_file, ckpt_file))
            facenet.load_model(trained_model_dir, meta_file, ckpt_file)


            # Get input and output tensors
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            print("images_placeholder and embeddings phase_train %s, %s and %s" % (images_placeholder, embeddings, phase_train_placeholder))

            image_size = images_placeholder.get_shape()[1]
            embedding_size = embeddings.get_shape()[1]
print('time of loading facenet feature extractor is %f' % (time.time() - st))



#@fn_timer
#@profile
def SceneDetection (firstFrame, currentFrame):
    print('Comparing the new frame with background frame to detect the changes in scenes...')
    st = time.time()
    # compute the absolute difference between the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, currentFrame)
    thresh = cv2.threshold(frameDelta, 60, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image

    thresh = cv2.dilate(thresh, None, iterations=2)
    #image, contours, _ 
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    count = 0 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! now the code just work for one contour !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_area:
            continue
        count += 1
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(currentFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

        # draw the text and timestamp on the frame
        cv2.putText(currentFrame, "Room Status: {}".format(text), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(currentFrame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, currentFrame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
    print('time of scene change detection is: %f' % (time.time() - st))
    return currentFrame, thresh, frameDelta, count


#@fn_timer   
#@profile
def FaceDetection(img):
    print('Detecting face in the image...')

    margin = 32
    image_size=160
    minsize = 20 # minimum size of face
    threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
    factor = 0.709 # scale factor
    st = time.time()
    bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
    nrof_faces = bounding_boxes.shape[0]
    if nrof_faces>0:
        det = bounding_boxes[:,0:4]
        img_size = np.asarray(img.shape)[0:2]
        if nrof_faces>1:
            bounding_box_size = (det[:,2]-det[:,0])*(det[:,3]-det[:,1])
            img_center = img_size / 2
            offsets = np.vstack([ (det[:,0]+det[:,2])/2-img_center[1], (det[:,1]+det[:,3])/2-img_center[0] ])
            offset_dist_squared = np.sum(np.power(offsets,2.0),0)
            index = np.argmax(bounding_box_size-offset_dist_squared*2.0) # some extra weight on the centering
            det = det[index,:]
        det = np.squeeze(det)
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0]-margin/2, 0)
        bb[1] = np.maximum(det[1]-margin/2, 0)
        bb[2] = np.minimum(det[2]+margin/2, img_size[1])
        bb[3] = np.minimum(det[3]+margin/2, img_size[0])
        cropped = img[bb[1]:bb[3],bb[0]:bb[2],:]
        scaled = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
    print('time of face detection is %f' % (time.time() - st))
    return scaled



#@fn_timer
#@profile
def getEmbedding(face_image):
    print('Getting face feature...')
    st = time.time()
    with graph.as_default():
        with sess.as_default():
            # preparing input image
            face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            face_image = facenet.prewhiten(face_image)
            face_image = face_image[np.newaxis, ...]
            
            # Run forward pass to calculate embeddings
            print('Generating embeddings from images...')
            #images = facenet.load_data(paths_batch, do_random_crop=False, do_random_flip=False, image_size=image_size, do_prewhiten=True)
            feed_dict = { images_placeholder:face_image, phase_train_placeholder:False}
            emb = sess.run(embeddings, feed_dict=feed_dict)
            print('time of feature extraction is %f' % (time.time() - st))
            return emb
        

#@fn_timer    
def main():
    firstFrame = cv2.imread(base_addr + 'bg.jpg')
    firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
    firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
    currentFrame_org = cv2.imread(base_addr + 'shahin.jpg')
    currentFrame = cv2.cvtColor(currentFrame_org, cv2.COLOR_BGR2GRAY)
    currentFrame = cv2.GaussianBlur(currentFrame, (21, 21), 0)
    currentFrame, thresh, frameDelta, count = SceneDetection(firstFrame, currentFrame)
    cv2.imwrite(base_addr + "Security Feed.jpg", currentFrame)
    cv2.imwrite(base_addr + "Thresh.jpg", thresh)
    cv2.imwrite(base_addr + "Frame Delta.jpg", frameDelta)
    if count>0:
        # !!!!!!!!!!!!!!!!!! it does not works for a frame containing many images !!!!!!!!!!!!!!!!!!11
        face = FaceDetection(currentFrame_org)
        cv2.imwrite(base_addr + "Detected Face.jpg", face)
        newEmb = getEmbedding(face)
        
        print('Post processing...')
        st = time.time()
        
        hostEmb = np.load(base_addr+'member1.npy')
        diff = np.subtract(newEmb, hostEmb)
        dist = np.sum(np.square(diff),1)
        #print (dist)
        #np.save('member1.npy',emb)
        if dist > threshold:
            print ('A new person is detected')
        else:
            print ('A member of home is in the scene')
            
        print('time of post processing is %f' % (time.time() - st))

        time.sleep(60)
        time.sleep(60)
        time.sleep(60)
        face1 = FaceDetection(currentFrame_org)

        cv2.imwrite(base_addr + "Detected Face1.jpg", face1)
        newEmb1 = getEmbedding(face1)

        print('Post processing...')
        st1 = time.time()

        hostEmb1 = np.load(base_addr+'member1.npy')
        diff1 = np.subtract(newEmb1, hostEmb1)
        dist1 = np.sum(np.square(diff1),1)
        #print (dist)
        #np.save('member1.npy',emb)
        if dist1 > threshold:
            print ('A new person is detected')
        else:
            print ('A member of home is in the scene')

        print('time of post processing is %f' % (time.time() - st))

    else:
        print ('The reason of changes in the scene is not existing a person')       
    
def test_function():
    main()









# In[ ]:



