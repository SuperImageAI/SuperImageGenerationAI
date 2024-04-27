
import torch.utils.data as data
import torchvision as tv
import torch
import numpy as np

from PIL import Image

# Image.open(false_path+false_list[2],mode='r')


class MyDataset(data.Dataset):
    def __init__(self, root, transforms):
        import os
        self.train_class = os.listdir(root)
        self.class_list = [os.path.join(root, k) for k in self.train_class]
        self.imgs = []
        for i, j in enumerate(self.class_list):
            imgs = os.listdir(j)
            self.temp = [(os.path.join(j, k), int(self.train_class[i])) for k in imgs]
            self.imgs += self.temp
        self.transforms = transforms

    def __getitem__(self, index):
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = 2300000000
        from PIL import ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img_path, label = self.imgs[index]
        pil_img = Image.open(img_path).convert('RGB')
        if self.transforms:
            img = self.transforms(pil_img)
        else:
            pil_img = np.asarray(pil_img)
            img = torch.from_numpy(pil_img)
        return img, label

    def __len__(self):
        return len(self.imgs)


