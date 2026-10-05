import numpy as np
from sklearn.linear_model import LinearRegression


def predict_performance(attendance_percentage, average_marks):
    """
    Simple ML-based performance prediction.

    The model uses attendance and average marks
    as input features.
    """

    # Training data
    X = np.array([
        [50, 40],
        [55, 45],
        [60, 50],
        [65, 55],
        [70, 60],
        [75, 65],
        [80, 70],
        [85, 75],
        [90, 80],
        [95, 90]
    ])

    # Performance scores
    y = np.array([
        40,
        45,
        50,
        55,
        60,
        65,
        70,
        78,
        85,
        92
    ])

    model = LinearRegression()

    model.fit(X, y)

    prediction = model.predict(
        [[attendance_percentage, average_marks]]
    )[0]

    prediction = max(0, min(100, prediction))

    return round(float(prediction), 2)


def get_performance_status(prediction):
    if prediction >= 80:
        return "Excellent"

    elif prediction >= 60:
        return "Good"

    elif prediction >= 40:
        return "Average"

    else:
        return "Needs Improvement"


def get_recommendation(attendance, marks):
    recommendations = []

    if attendance < 75:
        recommendations.append(
            "Attendance is below 75%. Attend more classes."
        )

    if marks < 40:
        recommendations.append(
            "Marks are low. Focus on the subjects and practice regularly."
        )

    elif marks < 60:
        recommendations.append(
            "Performance is average. More practice can improve results."
        )

    else:
        recommendations.append(
            "Academic performance is good. Keep maintaining consistency."
        )

    if not recommendations:
        recommendations.append(
            "Keep working consistently."
        )

    return recommendations