import numpy as np
import torch.utils.data
import h5py
from fastai.vision import *
import os

class MaskImage(Image):    
    def show(self, **kwargs):
        show_image(Image(1- self.data/self.data.max()), **kwargs)
        
    def reconstruct(self, t):
        return MaskImage(t)


def get_y_fn(i):
    t = torch.tensor(depthData[int(i.stem)])
    t = t.expand(3,-1,-1)
    return MaskImage(t)

print("Loading Depth Model")
dst = '/home/h/.fastai/data/nyu_depth_v2_labeled.mat'
f = h5py.File(dst,'r')
depthData = np.array(f['depths']).transpose(0,2,1)
path_img = '/home/h/work/ml/course-v3/nbs/dl1/experiments/depth_perception/images'
tfms = get_transforms(max_lighting=None)
data = (ImageImageList.from_folder(path_img, extensions='.jpg')
        .split_by_rand_pct(0.2, seed=44)
        .label_from_func(get_y_fn, label_cls=ItemList)
        .transform(tfms, size=220, tfm_y=True)
        .databunch(bs=10).normalize(imagenet_stats)
)
data.c = 3
learn = unet_learner(data, models.resnet50, loss_func=mse)
torch.tensor([x.px.max() for x in learn.data.y]).max()
p = os.path.abspath('./ml/depth/model_best')
learn.load(p)
print("Finished")

def predict_depth(img):
    img = img[:,:,::-1].transpose((2,0,1)).copy()
    img = torch.from_numpy(img).float().div(255.)
    pred = learn.predict(Image(img))[0].data
    pred = pred*25.5
    return pred.numpy().transpose((1, 2, 0)).astype(np.uint8)

