from pathlib import Path


def test_preprocess_validates_file(tmp_path):
    image_path = tmp_path / "sample.png"
    from PIL import Image
    Image.new("RGB", (224, 224), color="white").save(image_path)

    from ml.preprocessing.preprocess import validate_image_file

    result = validate_image_file(image_path)
    assert result.valid is True
    assert result.width == 224
    assert result.height == 224


def test_model_loads_and_runs():
    from ml.models.dental_age_model import TinyDentalRegressor
    model = TinyDentalRegressor(input_channels=1)
    x = model(torch.ones(2, 1, 224, 224))
    assert x.shape == (2,)


def test_inference_returns_numeric():
    from ml.inference.inference import DentalAgePredictor, ensure_model_exists
    model_path = Path("ml/weights/best_model.pth")
    ensure_model_exists(model_path)
    from PIL import Image
    image_path = Path("/tmp/dental-dev-test.png")
    Image.new("L", (224, 224), 128).save(image_path)
    predictor = DentalAgePredictor(model_path)
    age = predictor.predict(image_path)
    assert isinstance(age, float)
    assert age > 0
