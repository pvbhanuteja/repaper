import easyocr
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon
from transformers import LayoutLMForTokenClassification, LayoutLMv2Processor

from .utils.form_utils import create_google_form


class Repaper(object):
    '''
    Repaper class to perform all the parse the form and apply desired methods
    '''

    def __init__(self, img_path, use_gpu=False):
        """ Initialize the client. Do this before using other Label Studio SDK classes and methods in your script.
        Parameters
        ----------
        img_path: Path
            Path to image
        use_gpu : Bool
            Bool parameter to use gpu
        """
        self.processor = LayoutLMv2Processor.from_pretrained(
            "pvbhanuteja/layoutlm-funsd")
        self.model = LayoutLMForTokenClassification.from_pretrained(
            "pvbhanuteja/layoutlm-funsd")
        self.image = Image.open(img_path)
        self.reader = easyocr.Reader(['en'], gpu=use_gpu)
        self.label2color = {
            "B-HEADER": "blue",
            "B-QUESTION": "red",
            "B-ANSWER": "green",
            "I-HEADER": "blue",
            "I-QUESTION": "red",
            "I-ANSWER": "green",
        }
        self.image = Image.open(img_path).convert("RGB")
        self.encoding = self.processor(self.image, return_tensors="pt")
        del self.encoding["image"]
        # run inference
        outputs = self.model(**self.encoding)
        predictions = outputs.logits.argmax(-1).squeeze().tolist()
        # get labels
        self.labels = [self.model.config.id2label[prediction]
                       for prediction in predictions]
        self.width, self.height = self.image.size

    def unnormalize_box(self, bbox, width, height):
        '''
        To unnormaize the normalized bouding boxes during prediction/inference
        '''
        return [
            width * (bbox[0] / 1000).numpy(),
            height * (bbox[1] / 1000).numpy(),
            width * (bbox[2] / 1000).numpy(),
            height * (bbox[3] / 1000).numpy(), ]

    def draw_boxes(self, image, boxes, predictions):
        '''
        Method to display prefictions on the input image returns PIL image with drawn bouding boxes
        '''
        width, height = image.size
        normalizes_boxes = [self.unnormalize_box(
            box, width, height) for box in boxes]

        # draw predictions over the image
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        for prediction, box in zip(predictions, normalizes_boxes):
            if prediction == "O":
                continue
            draw.rectangle(box, outline="black")
            draw.rectangle(box, outline=self.label2color[prediction])
            draw.text((box[0] + 10, box[1] - 10), text=prediction,
                      fill=self.label2color[prediction], font=font)
        return image

    def draw_predictions_image(self, img_save=False, out_file_name='out'):
        '''
        Returns a PIL image
        '''
        image = self.draw_boxes(
            self.image, self.encoding["bbox"][0], self.labels)

        if img_save:
            image.save(f'''{out_file_name}.jpg''')
        return image

    def get_headers_questions(self):
        '''
        Get set of all questions and headers from the document.
        '''
        width, height = self.image.size
        normalizes_boxes = [self.unnormalize_box(
            box, width, height) for box in self.encoding["bbox"][0]]
        questions = []
        headers = []
        prev_box = [0, 0, 0, 0]
        first = True
        pre_begin = ''
        pre_entity = ''
        pre_str = ''
        for sample in zip(self.labels[1:-1], normalizes_boxes[1:-1]):
            if sample[0] != 'O':
                if self.calculate_iou(prev_box, sample[1]) != 0.0:
                    prev_box = sample[1]
                else:
                    cropped_image1 = self.image.crop(
                        np.add(sample[1], [-5, -5, 5, 5]))
                    result = self.reader.readtext(
                        np.array(cropped_image1), detail=0)
                    begin, entity = sample[0].split('-')
                    if first:
                        first = False
                        pre_begin = begin
                        pre_entity = entity
                        if entity == "HEADER" or entity == "QUESTION":
                            pre_entity = entity
                        pre_str = result[0] if len(result) > 0 else ' '
                    else:
                        if entity != pre_entity:
                            if pre_entity == "HEADER":
                                headers.append(pre_str)
                            if pre_entity == "QUESTION":
                                questions.append(pre_str)
                            pre_str = result[0] if len(result) > 0 else ' '
                        if entity == pre_entity and begin == "I":
                            pre_str = pre_str + ' ' + \
                                (result[0] if len(result) > 0 else ' ')
                        if entity == pre_entity and begin == "B":
                            if pre_entity == "HEADER":
                                headers.append(pre_str)
                            if pre_entity == "QUESTION":
                                questions.append(pre_str)
                            pre_str = result[0] if len(result) > 0 else ' '
                        pre_begin = begin
                        pre_entity = entity
                    prev_box = sample[1]
        return (questions, headers)

    def calculate_iou(self, box_1, box_2):
        '''
        Calculate IOU score between 2 bounding boxes with [x1,y1,x4,y4]
        coordination system (x1,y1) is top left point and (x4,y4) is bottom-
        right point 
        '''
        box_1 = [[box_1[0], box_1[1]], [box_1[2], box_1[1]],
                 [box_1[2], box_1[3]], [box_1[0], box_1[3]]]
        box_2 = [[box_2[0], box_2[1]], [box_2[2], box_2[1]],
                 [box_2[2], box_2[3]], [box_2[0], box_2[3]]]

        poly_1 = Polygon(box_1)
        poly_2 = Polygon(box_2)
        iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
        return iou

    # def make_editable_pdf(self, pdf_save_path):
    #     '''
    #     Helper function to generate editable PDF from the input image form
    #     Args:
    #         pdf_save_path (path) : Path to save PDF
    #     '''
    #     c = canvas.Canvas(pdf_save_path, pagesize=(self.width, self.height))
    #     form = c.acroForm
    #     cn = 0
    #     for prediction, box in zip(self.true_predictions[1:-1], self.true_boxes[1:-1]):
    #         print(prediction)
    #         predicted_label = prediction[2:].lower()
    #         if predicted_label != 'answer':
    #             c.drawString(box[0], self.height - box[1], self.words[cn])
    #             cn += 1
    #         else:
    #             form.textfield(name=self.words[cn],
    #                            x=box[0], y=self.height - box[1], borderStyle='inset',
    #                            width=box[2], forceBorder=True)
    #             cn += 1
    #     c.save()
    #     return ('pdf saved')

    def make_google_from(self, path_to_client_json):
        """This generates google form from the document
        Args:
            path_to_client_json (pagh): Path to OAuth client secrete file
            check this example to generate the json file https://developers.google.com/forms/api/quickstart/python#set_up_your_environment
        """
        questions, headers = self.get_headers_questions()

        from_id = create_google_form(
            path_to_client_json, questions, " ".join(headers))
        # print(f'''Form created with form id: {from_id["formId"]} and is accessible at: \n https://docs.google.com/forms/d/{from_id['formId']}/viewform \n
        # edit and publish the form to make it accessible to others''')
        return from_id


if __name__ == '__main__':
    pp = Repaper(
        '/mnt/nvme-data1/bhanu/code-bases/papertoweb/samples/test.jpg')
    # pp.make_editable_pdf('/mnt/nvme-data1/bhanu/code-bases/papertoweb/outputs/sample_form.pdf')
    print(pp.get_headers_questions())
    # pp.draw_predictions_image(img_save=True)
    print(pp.make_google_from(
        '/mnt/nvme-data1/bhanu/code-bases/papertoweb/client_secret.json'))
