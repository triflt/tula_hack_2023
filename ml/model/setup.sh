pip install "git+https://github.com/facebookresearch/segment-anything.git"
pip install jupyter_bbox_widget roboflow dataclasses-json supervision
mkdir weights
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -P weights

pip install -r requirements.txt