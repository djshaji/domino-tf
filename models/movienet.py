import pathlib, sys, os
from PIL import Image
from matplotlib import cm

import matplotlib as mpl
import matplotlib.pyplot as plt
import mediapy as media
import numpy as np
import PIL

import tensorflow as tf
import tensorflow_io as tfio
import tensorflow_hub as hub
import tqdm
# Read and process a video
def load_gif(file_path, image_size=(224, 224)):
  """Loads a gif file into a TF tensor.

  Use images resized to match what's expected by your model.
  The model pages say the "A2" models expect 224 x 224 images at 5 fps

  Args:
    file_path: path to the location of a gif file.
    image_size: a tuple of target size.

  Returns:
    a video of the gif file
  """
  # Load a gif file, convert it to a TF tensor
  raw = tf.io.read_file(file_path)
  #video = tf.io.decode_gif(raw)
  video = tfio.experimental.ffmpeg.decode_video(raw, index=0, name=None)

  # Resize the video
  video = tf.image.resize(video, image_size)
  # change dtype to a float32
  # Hub models always want images normalized to [0,1]
  # ref: https://www.tensorflow.org/hub/common_signatures/images#input
  video = tf.cast(video, tf.float32) / 255.
  return video
  
#jumpingjack=load_gif(jumpingjack_path)
#jumpingjack.shape

# Get top_k labels and probabilities

class MoviNet:
    mpl.rcParams.update({
        'font.size': 10,
    })

    labels_path = tf.keras.utils.get_file(
        fname='labels.txt',
        origin='https://raw.githubusercontent.com/tensorflow/models/f8af2291cced43fc9f1d9b41ddbf772ae7b0d7d2/official/projects/movinet/files/kinetics_600_labels.txt'
    )
    labels_path = pathlib.Path(labels_path)

    lines = labels_path.read_text().splitlines()
    KINETICS_600_LABELS = np.array([line.strip() for line in lines])
    KINETICS_600_LABELS[:20]

    def get_top_k(self, probs, k=5, label_map=KINETICS_600_LABELS):
      """Outputs the top k model labels and probabilities on the given video.

      Args:
        probs: probability tensor of shape (num_frames, num_classes) that represents
          the probability of each class on each frame.
        k: the number of top predictions to select.
        label_map: a list of labels to map logit indices to label strings.

      Returns:
        a tuple of the top-k labels and probabilities.
      """
      # Sort predictions to find top_k
      top_predictions = tf.argsort(probs, axis=-1, direction='DESCENDING')[:k]
      # collect the labels of top_k predictions
      top_labels = tf.gather(label_map, top_predictions, axis=-1)
      # decode lablels
      top_labels = [label.decode('utf8') for label in top_labels.numpy()]
      # top_k probabilities of the predictions
      top_probs = tf.gather(probs, top_predictions, axis=-1).numpy()
      return tuple(zip(top_labels, top_probs))

    def load_file (self, url):
        #self.jumpingjack_url = 'https://github.com/tensorflow/models/raw/f8af2291cced43fc9f1d9b41ddbf772ae7b0d7d2/official/projects/movinet/files/jumpingjack.gif'
        self.jumpingjack_url = url
        self.jumpingjack_path = tf.keras.utils.get_file(
            fname=os.path.basename (self.jumpingjack_url),
            origin=self.jumpingjack_url,
            cache_dir='cache', cache_subdir='cache',
        )
    
        self.jumpingjack=load_gif(self.jumpingjack_path)


      
    id = 'a2'
    mode = 'stream'
    version = '3'
    hub_url = f'models/compiled/movinet/'
    model = hub.load(hub_url)

    list(model.signatures.keys())

    lines = model.signatures['init_states'].pretty_printed_signature().splitlines()
    lines = lines[:10]
    lines.append('      ...')
    print('.\n'.join(lines))

    def detect (self, gtk3 = None):
        initial_state = self.model.init_states(self.jumpingjack[tf.newaxis, ...].shape)
        inputs = initial_state.copy()

        # Add the batch axis, take the first frme, but keep the frame-axis.
        inputs['image'] = self.jumpingjack[tf.newaxis, 0:1, ...] 

        # warmup
        self.model(inputs);

        logits, new_state = self.model(inputs)
        logits = logits[0]
        probs = tf.nn.softmax(logits, axis=-1)

        for label, p in self.get_top_k(probs):
          print(f'{label:20s}: {p:.3f}')

        print()

        state = initial_state.copy()
        all_logits = []

        for n in range(len(self.jumpingjack)):
          inputs = state
          inputs['image'] = self.jumpingjack[tf.newaxis, n:n+1, ...]
          result, state = self.model(inputs)
          all_logits.append(logits)
          if gtk3 is not None:
              im = Image.fromarray(np.uint8((self.jumpingjack [n])*255))
              #_p = gtk3.pillow_to_pixbuf (im)
              gtk3.set_image (im)

        probabilities = tf.nn.softmax(all_logits, axis=-1)

        for label, p in self.get_top_k(probabilities[-1]):
          print(f'{label:20s}: {p:.3f}')
          
        for label, p in self.get_top_k(tf.reduce_mean(probabilities, axis=0)):
          print(f'{label:20s}: {p:.3f}')
