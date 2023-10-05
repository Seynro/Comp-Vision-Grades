from Grading_2_1 import TestGrader
from split_image_1_1 import ImageSplitter



class Grading:

    def __init__(self,image_path: str, save_path: str):
        self.image_path = image_path
        self.save_path = save_path


    def __call__(self):

        splitter = ImageSplitter(self.image_path, self.save_path)
        splitter()

        if self.image_path.endswith(".png"):
            image_path_ans = self.image_path.replace(".png", f"_ans.png")
            output_path = self.image_path.replace(".png", f"_RESULT.png")
        elif self.image_path.endswith(".jpg"):
            image_path_ans = self.image_path.replace(".jpg", f"_ans.jpg")
            output_path = self.image_path.replace(".jpg", f"_RESULT.jpg")

        grader = TestGrader(image_path_ans, output_path)
        grader()


image_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_1.jpg"
save_path = r"C:\Users\user\Desktop\Programs\Python\Comp-Vision-Grades\main_test\test_1"

obj = Grading(image_path, save_path)
obj()