class Classifier():
    def __init__(self, model):
        self.model = model
        self.model.eval()
    def score(self, image, bbox, device):
        self.model.to(device)
        image.to(device)

        x1, y1, h, w = bbox
        cut_image = image[:, x1:x1 + h, y1:y1 + w]

        scores = self.model(cut_image).argmax(dim=-1)

        return scores