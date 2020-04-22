#pmd_module
#____________________________________________________________________________________________
import os
from tensorflow.keras.preprocessing.image import load_img,img_to_array,array_to_img,save_img
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

# Model Loading Library
from tensorflow.keras.models import load_model,model_from_json

#=============================================================================================

# ____________________________Image_Loader___________________________________________________
def get_image(imageName):																	  #|
  path_to_img = imageName #os.path.join(os.getcwd(),f'static/images/{imageName}')             #|
  img=load_img(path_to_img)																	  #|
  #display(img)																				  #|
  img_arr=np.resize(img_to_array(img),[128,128,3])											  #|
  img_arr=img_arr.reshape(1,128,128,3).astype("float32")/255								  #|
  return img_arr																			  #|									  
#_____________________________________________________________________________________________#|



#________________________________PMD_DECODER________________________________________________

def pmdDecoder(class_names):
  LE=LabelEncoder()
  #label encoding
  L_encd=LE.fit_transform(class_names)
  #print(L_encd)
  no_of_cls=len(L_encd)
  #onehot encoding on label encoded 
  ohEnc=to_categorical(L_encd,no_of_cls)
  pmdEnc={}
  for i,j in zip(class_names,ohEnc):
    pmdEnc[str(j)]=i
  print(pmdEnc)
  return pmdEnc

#========================================================================================

#_______________________________Predict_Function_______________________________________________________

def predict_the_class(image):
  global model
  class_names=class_names=['forest','snow_covered_land','grass_land','buildings','water','barren_land']
  predicted_result_encoded=model.predict(image)
  predicted_result=[round(i,0) for i in predicted_result_encoded[0]]
  pred_np_arr=np.array(predicted_result,dtype="float32")
  decoder=pmdDecoder(class_names)
  try:
    return decoder[str(pred_np_arr)]
  except:
    return "Unknown category\nSorry!:("
#_________________________________________________________________________________________________________

#___________________PMD_MOdel_____________________________________________________________________________
def load_PMD_model():
  #JSON
  # load json and create model
  model_dir=os.path.join(os.getcwd(),'model',"Final_model_v1.json")
  json_file = open(model_dir, 'r')
  loaded_model_json = json_file.read()
  json_file.close()
  loaded_model = model_from_json(loaded_model_json)
  # load weights into new model
  loaded_model.load_weights(os.path.join(os.getcwd(),'model',"weights_for_jsonModel.h5"))
  loaded_model.compile(loss="categorical_crossentropy",metrics=['accuracy'],optimizer="adam")
  global model
  model = loaded_model
  #model.summary()
  return loaded_model
#___________________________________________________________________________________________________________