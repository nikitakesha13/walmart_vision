from ergonomics.reba import RebaScore
import numpy as np

class REBA():
    def __init__(self, _points, _model):
        self.points = _points
        self.model = _model
        self.rebaScore = RebaScore()

    def normalize_data(self):
        self.points = (self.points - np.min(self.points)) / (np.max(self.points) - np.min(self.points))

    def calculate_risk(self):

        if not None in self.points :
            self.normalize_data()
            self.points = np.array([ [point[0], (-1) * point[1], 1] for point in self.points ])

            body_params = self.rebaScore.get_body_angles_from_pose_right(self.points)
            arms_params = self.rebaScore.get_arms_angles_from_pose_right(self.points)

            self.rebaScore.set_body(body_params)
            score_a, partial_a = self.rebaScore.compute_score_a()

            self.rebaScore.set_arms(arms_params)
            score_b, partial_b = self.rebaScore.compute_score_b()

            score_c, caption = self.rebaScore.compute_score_c(score_a, score_b)

            return (score_c, caption)
        
        return None